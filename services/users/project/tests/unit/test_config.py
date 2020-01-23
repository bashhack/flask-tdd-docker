import os


def test_postgres_host(test_app):
    assert test_app.config["POSTGRES_HOST"] == os.environ.get("POSTGRES_HOST")


def test_development_config(test_app):
    test_app.config.from_object("project.config.DevelopmentConfig")
    assert test_app.config["POSTGRES_HOST"] == os.environ.get("POSTGRES_HOST")
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000


def test_testing_config(test_app):
    test_app.config.from_object("project.config.TestingConfig")
    assert test_app.config["POSTGRES_HOST"] == os.environ.get("POSTGRES_HOST")
    assert test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_TEST_URL"
    )
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4


def test_production_config(test_app):
    test_app.config.from_object("project.config.ProductionConfig")
    assert test_app.config["POSTGRES_HOST"] == os.environ.get("POSTGRES_HOST")
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 13
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000
