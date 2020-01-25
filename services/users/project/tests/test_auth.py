import json

import pytest

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
