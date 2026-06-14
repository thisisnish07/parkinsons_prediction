import os

from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from flasgger import Swagger

from config import Config
from database.db import init_db
from middleware.error_handler import register_error_handlers
from routes import register_routes
from services.logging_service import setup_logging


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    web_dir = os.path.join(os.path.dirname(__file__), "web")

    @app.get("/")
    def serve_landing():
        return send_from_directory(web_dir, "landing.html")

    @app.get("/dashboard")
    def serve_dashboard():
        return send_from_directory(web_dir, "dashboard.html")

    @app.get("/prediction")
    def serve_prediction():
        return send_from_directory(web_dir, "prediction.html")

    setup_logging(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    Limiter(get_remote_address, app=app, default_limits=[app.config["RATE_LIMIT"]])

    api = Api(app)
    register_routes(api)
    register_error_handlers(app)

    Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "Parkinson's Prediction API",
                "version": app.config["APP_VERSION"],
            },
            "basePath": "/",
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Bearer <token>",
                }
            },
        },
    )

    init_db(app)
    return app


app = create_app()


if __name__ == "__main__":
    port = int(app.config.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
