import logging

import pandas as pd
from flask import request

from database.db import db
from database.models import AuditLog, PredictionHistory
from services.model_service import get_feature_names, get_model_version, load_model
from utils.helpers import utc_now_iso
from utils.validators import validate_prediction_payload


def predict(payload, user_id):
    feature_names = get_feature_names()
    is_valid, errors = validate_prediction_payload(payload, feature_names)
    if not is_valid:
        return None, errors

    model = load_model()
    data = pd.DataFrame([[payload[name] for name in feature_names]], columns=feature_names)

    try:
        proba = model.predict_proba(data)[0]
        prediction = int(proba.argmax())
        confidence = float(proba[prediction])
    except Exception:
        preds = model.predict(data)
        prediction = int(preds[0])
        confidence = 0.5

    risk_level = "high" if prediction == 1 and confidence >= 0.75 else "low"
    if confidence < 0.75:
        risk_level = "medium"

    history = PredictionHistory(
        user_id=user_id,
        input_data=payload,
        prediction=prediction,
        confidence=confidence,
        risk_level=risk_level,
        model_version=get_model_version(),
    )
    db.session.add(history)

    audit = AuditLog(
        user_id=user_id,
        action="prediction",
        details={"timestamp": utc_now_iso()},
        ip_address=request.remote_addr,
    )
    db.session.add(audit)
    db.session.commit()

    logging.info("Prediction completed for user %s", user_id)
    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk_level": risk_level,
        "timestamp": utc_now_iso(),
        "model_version": get_model_version(),
    }, None
