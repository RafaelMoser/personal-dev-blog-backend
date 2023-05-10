from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_pymongo import ObjectId
from schemas import ArticleSchema, PageCountSchema
from datetime import datetime
from nanoid import generate

from db import mongo

PAGE_SIZE = 5
TIMEZONE = "BRT"
article = Blueprint("articles", __name__, description="Articles")


@article.route("/newarticle/dummy")
class PublishArticle(MethodView):
    def get(this):
        nanoId = generate(size=6)
        while mongo.db.articles.count_documents({"nanoId": nanoId}) != 0:
            nanoId = generate(size=6)
        currentDateTime = datetime.now()
        publishDate = (
            f"{currentDateTime.year}/{currentDateTime.month}/{currentDateTime.day}"
        )
        publishTime = f"{currentDateTime.hour}:{currentDateTime.minute} {TIMEZONE}"
        article = {
            "title": "article title " + nanoId,
            "articleBody": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!\n"
            + "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!\n"
            + "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!",
            "publishDate": publishDate,
            "publishTime": publishTime,
            "nanoId": nanoId,
        }
        try:
            mongo.db.articles.insert_one(article)
            return {
                "title": article["title"],
                "nanoId": article["nanoId"],
                "publishTime": publishTime,
            }
        except Exception as error:
            print(error)
            return jsonify({"E": error.__str__})


@article.route("/article/list/<int:page>")
class ArticleListPage(MethodView):
    @article.response(200, ArticleSchema(many=True))
    def get(this, page):
        offset = (page - 1) * PAGE_SIZE
        return [
            i
            for i in mongo.db.articles.find().sort("publishDate", -1)[
                offset : offset + PAGE_SIZE
            ]
        ]


@article.route("/article/<string:article_id>")
class SingleArticle(MethodView):
    @article.response(200)
    def get(this, article_id):
        article = mongo.db.get_collection("articles").find_one({"nanoid": article_id})
        return article


@article.route("/article/pageCount")
class PageCount(MethodView):
    @article.response(200, PageCountSchema)
    def get(this):
        return {"pageCount": mongo.db.articles.count_documents({})}
