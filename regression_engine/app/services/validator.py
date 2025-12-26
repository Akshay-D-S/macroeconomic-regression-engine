def validate_metrics(metrics, thresholds):

    if metrics["r2"] < thresholds["min_r2"]:
        return False

    if metrics["adj_r2"] < thresholds["min_adj_r2"]:
        return False

    if metrics["multiple_r"] < thresholds["min_multiple_r"]:
        return False

    if any(p > thresholds["max_pvalue"] for p in metrics["pvalues"].values()):
        return False

    if any(v > thresholds["max_vif"] for v in metrics["vif"].values()):
        return False

    return True
