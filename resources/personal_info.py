from flask.views import MethodView
from flask_smorest import Blueprint
from flask_pymongo import ObjectId

from db import mongo
from schemas import BlogInfoSchema

PERSONAL_INFO_ID = ObjectId("645692cc0b436ad55e7c0f1d")

personalInfo = Blueprint("personalInfo", __name__, description="Personal Information")


@personalInfo.route("/aboutme/")
class ProfilePicture(MethodView):
    @personalInfo.response(200, BlogInfoSchema)
    def get(self):
        return mongo.db.get_collection("personal-info").find_one(
            {"_id": PERSONAL_INFO_ID}
        )
