from app.core.celery_app import celery_app
from app.core.redis import redis_client

from app.services.utils import get_calculation_columns, derive_corr_from_vif
from app.services.pruning import has_low_variance, has_high_collinearity, max_possible_r2
from app.services.metrics import calculate_metrics
from app.services.combination_engine import generate_combinations
from app.services.regression_engine import evaluate_combination
from app.services.validator import validate_metrics

import pandas as pd
import math
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def regression_task(self, payload):
    logger.info("Task started")
    logger.info(f"PAYLOAD>>{payload}")

    df = pd.DataFrame(payload["dataframe"])
    calc_names = get_calculation_columns(df)

    # 🔹 Fixed dependent variable
    Y_range = payload["delta_dr"]
    logger.info(f"Y range >>{Y_range}")
    if Y_range is None:
        logger.error("Y range missing in payload")
        return []

    Y_range = pd.Series(Y_range)

    if Y_range.isnull().any():
        logger.error("Y contains null values")
        return []

    if len(Y_range) != len(df):
        logger.error(
            "Y length (%d) does not match dataframe rows (%d)",
            len(Y_range), len(df)
        )
        return []

    redis_client.hset(
        f"task:{self.request.id}",
        mapping={"state": "STARTED", "percent": 0}
    )

    thresholds = payload["thresholds"]
    k = payload["combination_size"]

    logger.info("Calc Named columns count: %d", len(calc_names))

    if len(calc_names) < k:
        logger.warning("Not enough columns for k=%d", k)
        return []

    total = math.comb(len(calc_names), k)
    processed = 0
    results = []

    corr_limit = derive_corr_from_vif(thresholds["max_vif"])

    logger.info("Total combinations: %d", total)

    for combo in generate_combinations(calc_names, k):
        processed += 1

        if processed % 1000 == 0:
            percent = int((processed / total) * 100)
            logger.info(
                "Processed %d / %d (%d%%)",
                processed, total, percent
            )

            redis_client.hset(
                f"task:{self.request.id}",
                mapping={
                    "state": "PROGRESS",
                    "percent": percent,
                    "processed": processed,
                    "total": total
                }
            )

        # ---- EARLY PRUNING ----
        # if has_low_variance(df, combo):
        #     continue

        # if has_high_collinearity(df, combo, corr_limit):
        #     continue

        # if max_possible_r2(df, Y_range, combo) < thresholds["min_r2"]:
        #     continue
        # ----------------------

        best = evaluate_combination(df, Y_range, combo)
        if not best:
            continue

        metrics = calculate_metrics(
            best["model"],
            Y_range,
            df,
            best["predictors"]
        )

        if validate_metrics(metrics, thresholds):
            results.append({
                "columns": combo,
                "metrics": metrics
            })

    redis_client.hset(
        f"task:{self.request.id}",
        mapping={"state": "SUCCESS", "percent": 100}
    )

    logger.info("Task finished. Valid models: %d", len(results))
    return results
