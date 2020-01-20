from flask.blueprints import Blueprint
from flask.globals import request
from flask_restplus import fields
from flask_restplus.api import Api
from flask_restplus.namespace import Namespace
from flask_restplus.resource import Resource

from project.api.users.services import (add_user, delete_user, get_all_users,
                                        get_user_by_email, get_user_by_id,
                                        update_user)

users_namespace = Namespace("users")

user = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UserList(Resource):
    @users_namespace.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_email(email)

        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        add_user(username, email)
        response_object["message"] = f"{email} was added!"
        return response_object, 201

    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        return get_all_users(), 200


users_namespace.add_resource(UserList, "")


class Users(Resource):
    @users_namespace.marshal_with(user)
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200

    @users_namespace.expect(user, validate=True)
    def put(self, user_id):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        update_user(user, username, email)
        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200

    def delete(self, user_id):
        response_object = {}
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        delete_user(user)
        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200


users_namespace.add_resource(Users, "/<int:user_id>")
