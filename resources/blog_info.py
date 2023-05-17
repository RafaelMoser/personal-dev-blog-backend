from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_pymongo import ObjectId
from jwt import jwt_required

from db import mongo
from schemas import BlogInfoSchema, BlogInfoUpdateSchema

BLOG_INFO_ID = ObjectId("645e4b2eafb760dd061db731")

blogInfo = Blueprint("personalInfo", __name__, description="Personal Information")


@blogInfo.route("/aboutme/")
class SidebarInfo(MethodView):
    @blogInfo.response(200, BlogInfoSchema)
    def get(self):
        return mongo.db.bloginfo.find_one({"_id": BLOG_INFO_ID})



@blogInfo.route("/admin/profile")
class BlogInfoUpdater(MethodView):
    @blogInfo.response(200, BlogInfoUpdateSchema)
    def get(self):
        return mongo.db.bloginfo.find_one({"_id": BLOG_INFO_ID})

    @jwt_required()
    @blogInfo.arguments(BlogInfoUpdateSchema)
    @blogInfo.response(21, BlogInfoUpdateSchema)
    def patch(self, update_data):
        try:
            mongo.db.bloginfo.update_one({"_id": BLOG_INFO_ID}, update_data)
            return update_data
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400

