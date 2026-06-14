import logging
import os
from logging.handlers import RotatingFileHandler

from flask import request


def setup_logging(app):
    log_dir = app.config["LOG_DIR"]
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"), maxBytes=5_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.handlers = [file_handler, stream_handler]

    @app.before_request
    def log_request():
        logging.info(
            "request %s %s from %s",
            request.method,
            request.path,
            request.remote_addr,
        )

    @app.after_request
    def log_response(response):
        logging.info("response %s %s", response.status_code, request.path)
        return response
