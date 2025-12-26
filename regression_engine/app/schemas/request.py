from pydantic import BaseModel, Field
from typing import Dict, List, Any

class RegressionRequest(BaseModel):
    delta_dr: List[float] = Field(
        ...,
        description="Dependent variable (Y)",
        example=[-55.13, -54.97, -54.75, -54.59]
    )

    dataframe: Dict[str, List[Any]] = Field(
        ...,
        description="Flattened regression feature matrix (X)",
        example={
            "delta_ME01__1": [38.6, 40.2, 41.1, 39.8],
            "delta_ME02__6": [53.3, 54.1, 55.0, 56.2],
            "delta_ME03__11": [2.02, 2.10, 2.15, 2.18]
        }
    )

    thresholds: Dict[str, float] = Field(
        ...,
        example={
            "min_r2": 0.65,
            "min_adj_r2": 0.65,
            "min_multiple_r": 0.65,
            "max_pvalue": 0.05,
            "max_vif": 4
        }
    )

    combination_size: int = Field(
        3,
        ge=2,
        le=5,
        description="Number of predictors per regression"
    )
