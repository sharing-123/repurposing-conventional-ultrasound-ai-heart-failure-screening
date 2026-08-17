import pandas as pd


def platform_delta(df: pd.DataFrame, score_col: str) -> pd.DataFrame:
    pivot = df.pivot(index="view", columns="platform", values=score_col)
    pivot["delta"] = pivot["High-end"] - pivot["Low-end"]
    return pivot.reset_index()


def best_row(df: pd.DataFrame, score_col: str) -> pd.Series:
    return df.loc[df[score_col].idxmax()]


def melt_rate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    rate_cols = ["sensitivity", "specificity", "ppv", "npv", "accuracy"]
    return df.melt(
        id_vars=["platform", "view"],
        value_vars=rate_cols,
        var_name="metric",
        value_name="value",
    )
