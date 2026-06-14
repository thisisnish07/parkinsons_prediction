import json
import os
import time

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.svm import SVC

from services.dataset_service import load_dataset
from training.evaluate import evaluate_model
from training.feature_engineering import get_feature_count
from training.preprocessing import clean_dataset, split_features_target


def _build_pipeline(model, k_best):
    return Pipeline(
        [
            ("scaler", MinMaxScaler()),
            ("selector", SelectKBest(score_func=chi2, k=k_best)),
            ("model", model),
        ]
    )


def _get_models():
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "svm": SVC(kernel="rbf", probability=True),
        "gradient_boosting": GradientBoostingClassifier(random_state=42),
    }

    try:
        from xgboost import XGBClassifier

        models["xgboost"] = XGBClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=4,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            use_label_encoder=False,
        )
    except Exception:
        pass

    return models


def train_and_save_models(dataset_path=None, output_dir=None):
    df = load_dataset(dataset_path)
    df = clean_dataset(df)

    x, y = split_features_target(df)
    feature_names = list(x.columns)

    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    k_best = get_feature_count(x_train.shape[1])

    best_model = None
    best_metrics = None
    best_name = None

    for name, model in _get_models().items():
        pipeline = _build_pipeline(model, k_best)
        pipeline.fit(x_train, y_train)
        metrics = evaluate_model(pipeline, x_val, y_val)

        if best_metrics is None or (metrics["roc_auc"] or 0) > (best_metrics["roc_auc"] or 0):
            best_metrics = metrics
            best_model = pipeline
            best_name = name

    if best_model is None:
        raise RuntimeError("No model trained successfully.")

    output_dir = output_dir or os.path.join(os.getcwd(), "trained_models")
    os.makedirs(output_dir, exist_ok=True)

    model_path = os.path.join(output_dir, "best_model.pkl")
    metadata_path = os.path.join(output_dir, "model_metadata.json")
    feature_path = os.path.join(output_dir, "feature_names.json")
    metrics_path = os.path.join(output_dir, "metrics.json")

    import joblib

    joblib.dump(best_model, model_path)

    model_version = str(int(time.time()))
    metadata = {
        "model_version": model_version,
        "model_type": best_name,
        "metrics": best_metrics,
    }

    with open(metadata_path, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    with open(feature_path, "w", encoding="utf-8") as handle:
        json.dump(feature_names, handle, indent=2)

    with open(metrics_path, "w", encoding="utf-8") as handle:
        json.dump(best_metrics, handle, indent=2)

    return {
        "model_version": model_version,
        "model_type": best_name,
        "metrics": best_metrics,
    }


if __name__ == "__main__":
    train_and_save_models()
