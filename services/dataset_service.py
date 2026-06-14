import os

import pandas as pd
from flask import current_app, has_app_context


def load_dataset(path=None):
    if path:
        dataset_path = path
    elif has_app_context():
        dataset_path = current_app.config["DATASET_PATH"]
    else:
        dataset_path = os.getenv("DATASET_PATH", "dataset/original_dataset.csv")

    df = pd.read_csv(dataset_path)
    if "status" not in df.columns:
        raise ValueError("Dataset must contain a 'status' column.")
    return df
