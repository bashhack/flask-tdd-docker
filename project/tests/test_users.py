import json

import pytest

from project import db
from project.api.models import User


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "testuser", "email": "testuser@example.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "testuser@example.com was added!" in data["message"]


@pytest.mark.parametrize(
    "payload, status_code, message",
    [
        [{}, 400, "Input payload validation failed"],
        [{"email": "foo"}, 400, "Input payload validation failed"],
    ],
)
def test_add_user_invalid(test_app, test_database, payload, status_code, message):
    client = test_app.test_client()
    resp = client.post(
        "/users", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]


def test_add_duplicate_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "testuser", "email": "testuser@example.com"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "testuser", "email": "testuser@example.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_get_user(test_app, test_database, add_user):
    user = add_user(username="testuser", email="testuser@example.com")
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "testuser" in data["username"]
    assert "testuser@example.com" in data["email"]


def test_get_user_does_not_exist(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_get_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("testuser1", "testuser1@example.com")
    add_user("testuser2", "testuser2@example.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "testuser1" in data[0]["username"]
    assert "testuser2" in data[1]["username"]
    assert "testuser1@example.com" in data[0]["email"]
    assert "testuser2@example.com" in data[1]["email"]


def test_delete_user(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("testuser1", "testuser1@example.com")
    client = test_app.test_client()

    # Confirm user exists...
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 1

    # Delete the user...
    resp = client.delete(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert f"{user.email} was removed!" in data["message"]

    # Confirm the user is then removed...
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 0


def test_delete_invalid(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("foo", "bar")
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_update_user(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("testuser1", "testuser1@example.com")
    client = test_app.test_client()
    updated_email = "updated-testuser1@example.com"
    resp = client.put(
        f"/users/{user.id}",
        data=json.dumps({"username": "testuser1", "email": updated_email}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert f"{user.id} was updated!" in data["message"]

    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert user.username in data["username"]
    assert updated_email in data["email"]


@pytest.mark.parametrize(
    "user_id, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [1, {"email": "testuser1@example.com"}, 400, "Input payload validation failed"],
        [999, {"username": "foo", "email": "bar"}, 404, "User 999 does not exist"],
    ],
)
def test_update_user_invalid(
    test_app, test_database, user_id, payload, status_code, message
):
    client = test_app.test_client()
    resp = client.put(
        f"/users/{user_id}", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
