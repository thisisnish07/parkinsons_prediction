from database.models import PredictionHistory
from services.model_service import load_metadata
from services.prediction_service import predict
from utils.response_formatter import error_response, success_response


def create_prediction(payload, user_id):
    result, errors = predict(payload, user_id)
    if errors:
        return error_response("Validation failed", 400, errors)
    return success_response(result, "Prediction successful")


def get_model_info():
    metadata = load_metadata()
    return success_response(metadata, "Model info")


def get_prediction_history(user_id):
    records = (
        PredictionHistory.query.filter_by(user_id=user_id)
        .order_by(PredictionHistory.created_at.desc())
        .limit(50)
        .all()
    )

    history = [
        {
            "prediction": record.prediction,
            "confidence": record.confidence,
            "risk_level": record.risk_level,
            "model_version": record.model_version,
            "created_at": record.created_at.isoformat() + "Z",
        }
        for record in records
    ]
    return success_response(history, "Prediction history")
