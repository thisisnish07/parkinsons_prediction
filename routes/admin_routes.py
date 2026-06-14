from flask_restful import Resource

from controllers import admin_controller
from middleware.auth_middleware import admin_required


class AdminRetrainResource(Resource):
    @admin_required
    def post(self):
        """
        Retrain the model pipeline.
        ---
        tags:
          - Admin
        security:
          - Bearer: []
        responses:
          200:
            description: Model retrained
        """
        return admin_controller.retrain()


class AdminSystemStatusResource(Resource):
    @admin_required
    def get(self):
        """
        Get system status.
        ---
        tags:
          - Admin
        security:
          - Bearer: []
        responses:
          200:
            description: Status response
        """
        return admin_controller.system_status()
