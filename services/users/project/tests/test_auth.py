import json

import pytest
from flask import current_app

from project.api.users.models import User


def test_user_registration(test_app, test_database):
    test_database.session.query(User).delete()
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {"username": "foo", "email": "foo@email.com", "password": "foobar"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert "foo" in data["username"]
    assert "foo@email.com" in data["email"]
    assert "foobar" not in data


def test_user_duplicate_email(test_app, test_database, add_user):
    add_user("foo", "foo@bar.com", "foobar")
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {"username": "foo", "email": "foo@email.com", "password": "foobar"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Sorry. That email already exists." in data["message"]


def test_user_duplicate_username(test_app, test_database, add_user):
    assert False


@pytest.mark.parametrize(
    "payload",
    [
        [{}],
        [{"email": "foo@bar.com", "password": "foobar"}],
        [{"username": "foo", "password": "foobar"}],
        [{"email": "foo@bar.com", "username": "foo"}],
    ],
)
def test_user_registration_invalid(test_app, test_database, payload):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Input payload validation failed" in data["message"]


def test_registered_user_login(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("foo", "foo@bar.com", "foobar")
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({"email": "foo@bar.com", "password": "foobar"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_non_registered_user_login(test_app, test_database):
    test_database.session.query(User).delete()
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({"email": "foo@bar.com", "password": "foobar"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert resp.content_type == "application/json"
    assert "User does not exist." in data["message"]


def test_valid_refresh(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("foo", "foo@bar.com", "foobar")
    client = test_app.test_client()

    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": user.email, "password": "foobar"}),
        content_type="application/json",
    )

    # valid refresh
    data = json.loads(resp_login.data.decode())
    refresh_token = json.loads(resp_login.data.decode())["refresh_token"]
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_invalid_refresh(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "Invalid"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Invalid token. Please log in again." in data["message"]


def test_invalid_refresh_expired_token(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    current_app.config["REFRESH_TOKEN_EXPIRATION"] = -1
    user = add_user("foo", "foo@bar.com", "foobar")
    client = test_app.test_client()

    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": user.email, "password": "foobar"}),
        content_type="application/json",
    )

    # invalid refresh
    refresh_token = json.loads(resp_login.data.decode())["refresh_token"]
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Signature expired. Please log in again." in data["message"]


def test_invalidate_refresh_token():
    # NOTE: Create new database table + only store a single refresh token per user
    assert False


def test_user_status(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("foo", "foo@bar.com", "foobar")
    client = test_app.test_client()

    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": user.email, "password": "foobar"}),
        content_type="application/json",
    )
    access_token = json.loads(resp_login.data.decode())["access_token"]

    resp = client.get(
        "/auth/status",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert user.username in data["username"]
    assert user.email in data["email"]
    assert "foobar" not in data


def test_invalid_status(test_app, test_database):
    client = test_app.test_client()
    resp = client.get(
        "/auth/status",
        headers={"Authorization": "Bearer invalid"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Invalid token. Please log in again." in data["message"]
