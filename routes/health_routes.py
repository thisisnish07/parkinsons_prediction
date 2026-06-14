from flask_restful import Resource

from utils.response_formatter import success_response


class HealthResource(Resource):
    def get(self):
        """
        Health check endpoint.
        ---
        tags:
          - Health
        responses:
          200:
            description: Service healthy
        """
        return success_response({"status": "ok"}, "Service healthy")
