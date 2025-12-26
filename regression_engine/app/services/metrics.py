import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


def calculate_metrics(model, y, df, predictors):
    """
    Calculate regression diagnostics for a fixed-Y regression
    """

    # --- Core metrics ---
    r2 = model.rsquared
    adj_r2 = model.rsquared_adj
    multiple_r = np.sqrt(max(r2, 0))

    # Exclude intercept from p-values
    pvalues = {
        k: float(v)
        for k, v in model.pvalues.items()
        if k != "const"
    }

    # --- VIF calculation ---
    X = df[list(predictors)]

    # Safety: remove constant columns
    X = X.loc[:, X.var() > 0]

    X_const = sm.add_constant(X)

    vif = {}
    for i, col in enumerate(X_const.columns):
        if col == "const":
            continue
        try:
            vif[col] = float(
                variance_inflation_factor(X_const.values, i)
            )
        except Exception:
            vif[col] = np.inf

    return {
        "r2": float(r2),
        "adj_r2": float(adj_r2),
        "multiple_r": float(multiple_r),
        "pvalues": pvalues,
        "vif": vif
    }
