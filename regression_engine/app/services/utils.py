import math
import ast
import pandas as pd


def get_calculation_columns(df):
    calc = []
    for col in df.columns:
        if isinstance(col, str) and "__" in col:
            left, right = col.rsplit("__", 1)
            if right.isdigit():
                calc.append(col)
    return calc

def derive_corr_from_vif(max_vif: float) -> float:
    if max_vif <= 1:
        return 0.0
    return math.sqrt(1 - 1 / max_vif)