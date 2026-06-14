import json
import os
import threading

import joblib
from flask import current_app

_model_lock = threading.Lock()
_cached_model = None
_cached_metadata = None
_cached_features = None


def load_model():
    global _cached_model
    if _cached_model is None:
        with _model_lock:
            if _cached_model is None:
                _cached_model = joblib.load(current_app.config["MODEL_PATH"])
    return _cached_model


def load_metadata():
    global _cached_metadata
    if _cached_metadata is None:
        path = current_app.config["MODEL_METADATA_PATH"]
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                _cached_metadata = json.load(handle)
        else:
            _cached_metadata = {}
    return _cached_metadata


def get_feature_names():
    global _cached_features
    if _cached_features is None:
        path = current_app.config["FEATURE_NAMES_PATH"]
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                _cached_features = json.load(handle)
        else:
            model = load_model()
            _cached_features = list(getattr(model, "feature_names_in_", []))
    return _cached_features


def get_model_version():
    metadata = load_metadata()
    return metadata.get("model_version", "unknown")
