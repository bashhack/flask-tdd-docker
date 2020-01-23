from project.api.users.models import User


def test_password_hashes_are_random(test_app, test_database, add_user):
    user_one = add_user("foo", "bar@baz.com", "foobar")
    user_two = add_user("foo2", "bar2@baz.com", "foobar")
    assert user_one.password != user_two.password


def test_encode_token(test_app, test_database, add_user):
    user = add_user("foo", "bar@baz.com", "foobar")
    token = user.encode_token(user.id, "access")
    assert isinstance(token, bytes)


def test_decode_token(test_app, test_database, add_user):
    user = add_user("foo", "bar@baz.com", "foobar")
    token = user.encode_token(user.id, "access")
    assert isinstance(token, bytes)
    assert User.decode_token(token) == user.id
