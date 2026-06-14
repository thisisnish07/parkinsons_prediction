from routes.admin_routes import AdminRetrainResource, AdminSystemStatusResource
from routes.auth_routes import LoginResource, RegisterResource
from routes.health_routes import HealthResource
from routes.prediction_routes import (
    ModelInfoResource,
    PredictResource,
    PredictionHistoryResource,
)


def register_routes(api):
    api.add_resource(HealthResource, "/api/health")

    api.add_resource(RegisterResource, "/api/auth/register")
    api.add_resource(LoginResource, "/api/auth/login")

    api.add_resource(PredictResource, "/api/predict")
    api.add_resource(ModelInfoResource, "/api/model-info")
    api.add_resource(PredictionHistoryResource, "/api/prediction-history")

    api.add_resource(AdminRetrainResource, "/api/admin/retrain-model")
    api.add_resource(AdminSystemStatusResource, "/api/admin/system-status")
