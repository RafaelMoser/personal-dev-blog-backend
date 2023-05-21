"""
user.py

login related API endpoints
"""

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from schemas import UserSchema
from blocklist import BLOCKLIST
import db

userLogin = Blueprint("Login", __name__, description="login API endpoint")


@userLogin.route("/login")
class UserLogin(MethodView):
    @userLogin.arguments(UserSchema)
    def post(self, user_data):
        user = db.get_user_data(user_data)
        if user and pbkdf2_sha256.verify(user_data["password"], user["password"]):
            access_token = create_access_token(
                identity=str(user["_id"]),
                fresh=True,
                expires_delta=timedelta(minutes=30),
            )
            refresh_token = create_refresh_token(
                identity=str(user["_id"]), expires_delta=timedelta(days=7)
            )
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Incorrect Username or password")


@userLogin.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, fresh=False, expires_delta=timedelta(minutes=30)
        )
        return {"access_token": new_token}


@userLogin.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfuly logged out."}


# @userLogin.route("/register")
class CreateUser(MethodView):
    @userLogin.arguments(UserSchema)
    def post(self, user_data):
        if db.user_exists(user_data["username"]):
            abort(409, message="An user with that name already exists")
        new_user_data = {
            "username": user_data["username"],
            "password": pbkdf2_sha256.hash(user_data["password"]),
        }
        db.register_user(new_user_data)
        return new_user_data
