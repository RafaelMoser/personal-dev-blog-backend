from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_pymongo import ObjectId
from schemas import ArticleSchema

from db import mongo

article = Blueprint("articles", __name__, description="Articles")


# @article.route("/newarticle/dummy")
# class PublishArticle(MethodView):
#     def get(this):
#         # request_data = request.get_json()
#         publishDate = datetime.datetime.now().__str__()
#         article = {
#             "title": "article title",
#             "articleBody": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!\n"
#             + "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!\n"
#             + "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!",
#             "publishDate": publishDate,
#         }
#         try:
#             result = mongo.db.articles.insert_one(article)
#             print(result.acknowledged)
#             return article["title"]
#         except Exception as error:
#             print(error)
#             return jsonify({"E": error.__str__})


@article.route("/article/list/<int:page>")
class ArticleListPage(MethodView):
    @article.response(200, ArticleSchema(many=True))
    def get(this, page):
        start = (page - 1) * 5
        end = page * 5
        return [i for i in mongo.db.articles.find().sort("publishDate", -1)[start:end]]


@article.route("/article/<string:article_id>")
class SingleArticle(MethodView):
    @article.response(200)
    def get(this, article_id):
        article = mongo.db.get_collection("articles").find_one(
            {"_id": ObjectId(article_id)}
        )
        print(article)
        return article
