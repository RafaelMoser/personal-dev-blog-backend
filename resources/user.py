from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from schemas import UserSchema
from db import mongo
from blocklist import BLOCKLIST
userLogin = Blueprint("Login", __name__, description="login API endpoint")


@userLogin.route("/login")
class UserLogin(MethodView):
    @userLogin.arguments(UserSchema)
    def post(self, user_data):
        user = mongo.db.users.find_one({"username": user_data["username"]})

        if user and pbkdf2_sha256.verify(user_data["password"], user["password"]):
            access_token = create_access_token(identity=str(user["_id"]))
            return {"access_token": access_token}, 200

        abort(401, message="Incorrect Username or password")

@userLogin.route("/logout")
class UserLogout(MethodView):
    @jwt_required
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfuly logged out."}