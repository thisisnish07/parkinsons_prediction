from flask import request
from flask_restful import Resource

from controllers import auth_controller


class RegisterResource(Resource):
    def post(self):
        """
        Register a new user.
        ---
        tags:
          - Authentication
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                  password:
                    type: string
        responses:
          201:
            description: User registered
        """
        data = request.get_json(silent=True) or {}
        return auth_controller.register(data)


class LoginResource(Resource):
    def post(self):
        """
        Login and receive a JWT token.
        ---
        tags:
          - Authentication
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                  password:
                    type: string
        responses:
          200:
            description: Login successful
        """
        data = request.get_json(silent=True) or {}
        return auth_controller.login(data)
