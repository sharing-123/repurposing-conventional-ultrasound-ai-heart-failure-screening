import pandas as pd

from config import BINARY_RESULTS_CSV, MULTICLASS_RESULTS_CSV, BASELINE_TEMPLATE_CSV, VIEW_ORDER, PLATFORM_ORDER


def load_binary_results() -> pd.DataFrame:
    df = pd.read_csv(BINARY_RESULTS_CSV)
    df["view"] = pd.Categorical(df["view"], categories=VIEW_ORDER, ordered=True)
    df["platform"] = pd.Categorical(df["platform"], categories=PLATFORM_ORDER, ordered=True)
    return df.sort_values(["view", "platform"]).reset_index(drop=True)


def load_multiclass_results() -> pd.DataFrame:
    df = pd.read_csv(MULTICLASS_RESULTS_CSV)
    df["view"] = pd.Categorical(df["view"], categories=VIEW_ORDER, ordered=True)
    df["platform"] = pd.Categorical(df["platform"], categories=PLATFORM_ORDER, ordered=True)
    return df.sort_values(["view", "platform"]).reset_index(drop=True)


def load_baseline_template() -> pd.DataFrame:
    return pd.read_csv(BASELINE_TEMPLATE_CSV)
