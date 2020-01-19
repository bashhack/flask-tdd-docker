import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
