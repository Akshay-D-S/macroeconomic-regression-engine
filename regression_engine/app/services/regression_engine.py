import statsmodels.api as sm
import pandas as pd

def evaluate_combination(df, y, predictors):

    X = df[list(predictors)]

    # Basic safety checks
    if X.isnull().any().any():
        return None

    if len(y) != len(X):
        return None

    X = sm.add_constant(X)

    try:
        model = sm.OLS(y, X).fit()
    except Exception:
        return None

    return {
        "predictors": predictors,
        "model": model
    }
