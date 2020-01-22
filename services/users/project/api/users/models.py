import os

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
        self.password = bcrypt.generate_password_hash(password).decode()

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
        }


if os.getenv("FLASK_ENV") == "development":
    from project import admin
    from project.api.users.admin import UsersAdminView

    admin.add_view(UsersAdminView(User, db.session))
