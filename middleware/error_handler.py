import logging

from utils.response_formatter import error_response


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(_error):
        return error_response("Bad request", 400)

    @app.errorhandler(401)
    def unauthorized(_error):
        return error_response("Unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(_error):
        return error_response("Forbidden", 403)

    @app.errorhandler(404)
    def not_found(_error):
        return error_response("Not found", 404)

    @app.errorhandler(500)
    def internal_error(error):
        logging.exception("Unhandled error: %s", error)
        return error_response("Internal server error", 500)
