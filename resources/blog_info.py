"""
blog_info.py

blog configuration and general data API endpoints
"""

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_pymongo import ObjectId
from jwt import jwt_required

from schemas import BlogInfoSchema, BlogInfoUpdateSchema
import db

blogInfo = Blueprint("personalInfo", __name__, description="Personal Information")

@blogInfo.route("/blogInfo/")
class SidebarInfo(MethodView):
    @blogInfo.response(200, BlogInfoSchema)
    def get(self):
        return db.get_blog_info()


@blogInfo.route("/aboutMe/")
class AboutMe(MethodView):
    @blogInfo.response(200, AboutMeSchema)
    def get(self):
        return db.get_blog_info()

@blogInfo.route("/admin/profile")
class BlogInfoUpdater(MethodView):
    @blogInfo.response(200, BlogInfoUpdateSchema)
    def get(self):
        return db.get_blog_info()

    @jwt_required()
    @blogInfo.arguments(BlogInfoUpdateSchema)
    @blogInfo.response(201, BlogInfoUpdateSchema)
    def patch(self, update_data):
        try:
            db.update_blog_info(update_data)
            return update_data
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400

