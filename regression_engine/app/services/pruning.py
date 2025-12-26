import numpy as np
import pandas as pd


def has_low_variance(df, cols, eps=1e-8):
    """
    Remove predictors with near-zero variance
    """
    for c in cols:
        if df[c].var() < eps:
            return True
    return False


def has_high_collinearity(df, cols, corr_limit):
    """
    Remove predictor sets with high inter-correlation
    (proxy for high VIF)
    """
    corr = df[list(cols)].corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    return (upper > corr_limit).any().any()


def max_possible_r2(df, y, cols):
    """
    Upper bound of achievable R² using correlation with Y.
    Uses max(|corr(X_i, Y)|)^2 as theoretical ceiling.
    """
    corrs = []

    for c in cols:
        if df[c].isnull().any() or y.isnull().any():
            continue

        r = np.corrcoef(df[c], y)[0, 1]

        if not np.isnan(r):
            corrs.append(abs(r))

    if not corrs:
        return 0.0

    return max(corrs) ** 2
