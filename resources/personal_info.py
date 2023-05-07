from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_pymongo import ObjectId
from time import sleep

from db import mongo

PERSONAL_INFO_ID = ObjectId("645692cc0b436ad55e7c0f1d")

personalInfo = Blueprint("personalInfo", __name__, description="Personal Information")


@personalInfo.route("/aboutme/")
class ProfilePicture(MethodView):
    def get(this):
        data = mongo.db.get_collection("personal-info").find_one(
            {"_id": PERSONAL_INFO_ID}
        )
        return jsonify(
            {
                "profileImageUrl": data["profileImageUrl"],
                "infoBlurb": data["infoBlurb"],
                "github": data["github"],
                "linkedIn": data["linkedin"],
            }
        )
