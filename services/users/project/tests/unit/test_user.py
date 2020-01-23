import json
from datetime import datetime

import pytest

import project.api.users.views


def test_add_user(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return None

    def mock_add_user(username, email, password):
        return True

    monkeypatch.setattr(
        project.api.users.views, "get_user_by_email", mock_get_user_by_email
    )
    monkeypatch.setattr(project.api.users.views, "add_user", mock_add_user)

    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "abxoebvaln",
            }
        ),
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
def test_add_user_invalid(test_app, payload, status_code, message):
    client = test_app.test_client()
    resp = client.post(
        "/users", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]


def test_add_duplicate_user(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return True

    def mock_add_user(username, email, password):
        return True

    monkeypatch.setattr(
        project.api.users.views, "get_user_by_email", mock_get_user_by_email
    )
    monkeypatch.setattr(project.api.users.views, "add_user", mock_add_user)

    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "abwocknslkj",
            }
        ),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "wbvoixbwmn",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_get_user(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return {
            "id": 1,
            "username": "mockuser",
            "email": "mock@user.com",
            "created_date": datetime.now(),
        }

    monkeypatch.setattr(project.api.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    resp = client.get(f"/users/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "mockuser" in data["username"]
    assert "mock@user.com" in data["email"]
    assert "password" not in data


def test_get_user_does_not_exist(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.api.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_get_all_users(test_app, monkeypatch):
    def mock_get_all_users():
        return [
            {
                "id": 1,
                "username": "mockuser1",
                "email": "mock@user1.com",
                "created_date": datetime.now(),
            },
            {
                "id": 2,
                "username": "mockuser2",
                "email": "mock@user2.com",
                "created_date": datetime.now(),
            },
        ]

    monkeypatch.setattr(project.api.users.views, "get_all_users", mock_get_all_users)

    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "mockuser1" in data[0]["username"]
    assert "mockuser2" in data[1]["username"]
    assert "mock@user1.com" in data[0]["email"]
    assert "mock@user2.com" in data[1]["email"]
    assert "password" not in data[0]
    assert "password" not in data[1]


def test_delete_user(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_user_by_id(user_id):
        d = AttrDict()
        d.update({"id": 1, "username": "mockuser", "email": "mock@user.com"})
        return d

    def mock_delete_user(user):
        return True

    monkeypatch.setattr(project.api.users.views, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(project.api.users.views, "delete_user", mock_delete_user)

    client = test_app.test_client()

    resp = client.delete(f"/users/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "mock@user.com was removed!" in data["message"]


def test_delete_invalid(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.api.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_update_user(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_user_by_id(user_id):
        d = AttrDict()
        d.update(
            {
                "id": 1,
                "username": "mockuser",
                "email": "mock@user.com",
                "created_date": datetime.now(),
            }
        )
        return d

    def mock_update_user(user, username, email):
        return True

    monkeypatch.setattr(project.api.users.views, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(project.api.users.views, "update_user", mock_update_user)

    client = test_app.test_client()
    updated_email = "mock@user.com"
    resp = client.put(
        f"/users/1",
        data=json.dumps(
            {"username": "mockuser", "email": updated_email}
        ),  # not sure if pass should be updated here...
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert f"1 was updated!" in data["message"]

    client = test_app.test_client()
    resp = client.get(f"/users/1")
    data = json.loads(resp.data.decode())
    assert "mockuser" in data["username"]
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
        test_app, monkeypatch, user_id, payload, status_code, message
):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.api.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    resp = client.put(
        f"/users/{user_id}", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
