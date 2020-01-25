from flask import request
from flask_bcrypt import check_password_hash
from flask_restplus import Namespace, Resource, fields

from project.api.users.services import add_user, get_user_by_email

auth_namespace = Namespace("auth")

user = auth_namespace.model(
    "User",
    {"username": fields.String(required=True), "email": fields.String(required=True)},
)

full_user = auth_namespace.inherit(
    "Full User", user, {"password": fields.String(required=True)}
)

login = auth_namespace.model(
    "User",
    {"email": fields.String(required=True), "password": fields.String(required=True)},
)
refresh = auth_namespace.model(
    "Refresh", {"refresh_token": fields.String(required=True)}
)
tokens = auth_namespace.inherit(
    "Access and refresh_tokens", refresh, {"access_token": fields.String(required=True)}
)


class Register(Resource):
    @auth_namespace.marshal_with(user)
    @auth_namespace.expect(full_user, validate=True)
    @auth_namespace.response(201, "Success")
    @auth_namespace.response(400, "Sorry. That email already exists.")
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")

        user = get_user_by_email(email)
        if user:
            auth_namespace.abort(400, "Sorry. That email already exists.")
        user = add_user(username, email, password)
        return user, 201


class Login(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(login, validate=True)
    @auth_namespace.response(200, "Success")
    @auth_namespace.response(404, "User does not exist.")
    def post(self):
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        user = get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            auth_namespace.abort(404, "User does not exist")

        access_token = user.encode_token(user.id, "access")
        refresh_token = user.encode_token(user.id, "refresh")
        response_object = {
            "access_token": access_token.decode(),
            "refresh_token": refresh_token.decode(),
        }
        return response_object, 200


class Refresh(Resource):
    def post(self):
        pass


class Status(Resource):
    def post(self):
        pass


auth_namespace.add_resource(Register, "/register")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
auth_namespace.add_resource(Status, "/status")
