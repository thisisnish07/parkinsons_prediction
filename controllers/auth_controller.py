from datetime import datetime, timedelta

import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import db
from database.models import AuditLog, User
from utils.response_formatter import error_response, success_response

def register(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response("Email and password required", 400)

    if User.query.filter_by(email=email).first():
        return error_response("User already exists", 409)

    # Use pbkdf2 to avoid hashlib.scrypt dependency issues in some environments.
    user = User(
        email=email,
        password_hash=generate_password_hash(password, method="pbkdf2:sha256"),
    )
    db.session.add(user)
    db.session.commit()

    db.session.add(AuditLog(user_id=user.id, action="register"))
    db.session.commit()

    return success_response({"user_id": user.id}, "User registered", 201)


def login(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response("Email and password required", 400)

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return error_response("Invalid credentials", 401)

    expires = datetime.utcnow() + timedelta(
        minutes=current_app.config["JWT_EXPIRES_MINUTES"]
    )
    token = jwt.encode(
        {"sub": user.id, "exp": expires},
        current_app.config["JWT_SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"],
    )

    db.session.add(AuditLog(user_id=user.id, action="login"))
    db.session.commit()

    return success_response({"token": token}, "Login successful")
