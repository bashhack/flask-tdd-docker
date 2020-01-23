import datetime
import os

import jwt
from flask import current_app
from flask.globals import current_app
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String

from project import bcrypt, db


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Boolean(), default=True, nullable=False)
    created_date = Column(DateTime, default=func.now(), nullable=False)

    def __init__(self, username="", email="", password=""):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config["BCRYPT_LOG_ROUNDS"]
        ).decode()

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
        }

    def encode_token(self, user_id, token_type):
        if token_type == "access":
            seconds = current_app.config.get("ACCESS_TOKEN_EXPIRATION")
        else:
            seconds = current_app.config.get("REFRESH_TOKEN_EXPIRATION")

        # expiration, issued at, subject
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=seconds),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(
            payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
        )

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, current_app.config.get("SECRET_KEY"))
        return payload.get("sub")


if os.getenv("FLASK_ENV") == "development":
    from project import admin
    from project.api.users.admin import UsersAdminView

    admin.add_view(UsersAdminView(User, db.session))
