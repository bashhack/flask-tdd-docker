from flask_sqlalchemy.model import Model
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    active = Column(Boolean(), default=True, nullable=False)
    created_date = Column(DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
