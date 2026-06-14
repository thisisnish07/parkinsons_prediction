from flask import g, request
from flask_restful import Resource

from controllers import prediction_controller
from middleware.auth_middleware import token_required


class PredictResource(Resource):
    @token_required
    def post(self):
        """
        Run a Parkinson's prediction.
        ---
        tags:
          - Prediction
        security:
          - Bearer: []
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
        responses:
          200:
            description: Prediction successful
        """
        payload = request.get_json(silent=True) or {}
        return prediction_controller.create_prediction(payload, g.current_user.id)


class ModelInfoResource(Resource):
    def get(self):
        """
        Get model metadata.
        ---
        tags:
          - Prediction
        responses:
          200:
            description: Model metadata
        """
        return prediction_controller.get_model_info()


class PredictionHistoryResource(Resource):
    @token_required
    def get(self):
        """
        Get prediction history for the current user.
        ---
        tags:
          - Prediction
        security:
          - Bearer: []
        responses:
          200:
            description: Prediction history
        """
        return prediction_controller.get_prediction_history(g.current_user.id)
