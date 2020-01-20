import json

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


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", data=json.dumps({}), content_type="application/json")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "testuser@example.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


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


def test_get_user_incorrect_id(test_app, test_database):
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
