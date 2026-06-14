from functools import wraps

import jwt
from flask import current_app, g, request

from database.models import User
from utils.response_formatter import error_response


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]

        if not token:
            return error_response("Missing or invalid token", 401)

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=[current_app.config["JWT_ALGORITHM"]],
            )
        except jwt.ExpiredSignatureError:
            return error_response("Token expired", 401)
        except jwt.InvalidTokenError:
            return error_response("Invalid token", 401)

        user = User.query.get(payload.get("sub"))
        if not user:
            return error_response("Invalid user", 401)

        g.current_user = user
        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_result = token_required(lambda *a, **k: None)()
        if auth_result is not None:
            return auth_result

        if not g.current_user.is_admin:
            return error_response("Admin access required", 403)

        return fn(*args, **kwargs)

    return wrapper
