from services.training_service import retrain_model
from utils.response_formatter import success_response


def retrain():
    result = retrain_model()
    return success_response(result, "Model retrained")


def system_status():
    return success_response({"status": "ok"}, "System status")
