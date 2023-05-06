from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_pymongo import ObjectId

from db import mongo

PERSONAL_INFO_ID = ObjectId("645692cc0b436ad55e7c0f1d")

blp = Blueprint("personalInfo", __name__, description="Personal Information")


@blp.route("/aboutme/image")
class ProfilePicture(MethodView):
    def get(this):
        data = mongo.db.get_collection("personal-info").find_one(
            {"_id": PERSONAL_INFO_ID}
        )
        return data["picture"]
