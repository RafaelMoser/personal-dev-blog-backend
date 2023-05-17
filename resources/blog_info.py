from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_pymongo import ObjectId

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

    def patch(self):
        data = request.json
        mongo.db.bloginfo.update_one({"_id": BLOG_INFO_ID}, data)
