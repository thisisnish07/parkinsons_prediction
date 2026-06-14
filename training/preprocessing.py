import pandas as pd


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    if "name" in df.columns:
        df = df.drop(columns=["name"])
    df = df.dropna().reset_index(drop=True)
    return df


def split_features_target(df: pd.DataFrame):
    features = df.drop(columns=["status"])
    target = df["status"]
    return features, target
