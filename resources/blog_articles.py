from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_pymongo import ObjectId
from schemas import ArticleSchema

from db import mongo

article = Blueprint("articles", __name__, description="Articles")


@article.route("/article/list/<int:page>")
class ArticleListPage(MethodView):
    @article.response(200, ArticleSchema(many=True))
    def get(this, page):
        return [i for i in mongo.db.get_collection("articles").find({})]


@article.route("/article/<string:article_id>")
class SingleArticle(MethodView):
    @article.response(200, ArticleSchema)
    def get(this, article_id):
        article = mongo.db.get_collection("articles").find_one(
            {"_id": ObjectId(article_id)}
        )
        print(article)
        return article

    @article.response(200, ArticleSchema)
    def post(this):
        pass
