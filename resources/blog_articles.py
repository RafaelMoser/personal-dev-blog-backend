from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import ArticleSchema, PageCountSchema, SingleArticleSchema
from datetime import datetime
from nanoid import generate
import math

from db import mongo

PAGE_SIZE = 3
TIMEZONE = "BRT"
article = Blueprint("articles", __name__, description="Articles")


@article.route("/newarticle/dummy")
class PublishArticle(MethodView):
    def get(this):
        nanoId = generate(size=6)
        while mongo.db.articles.count_documents({"nanoId": nanoId}) != 0:
            nanoId = generate(size=6)
        currentDateTime = datetime.now()
        article = {
            "title": "article title " + nanoId,
            "articleBody": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!\n"
            + "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!\n"
            + "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam id voluptatibus numquam temporibus iure ipsum architecto nobis suscipit, veniam fugiat qui ex a aperiam maiores aut quaerat. Temporibus, architecto natus!",
            "publishDateTime": currentDateTime.isoformat(),
            "nanoId": nanoId,
        }
        try:
            mongo.db.articles.insert_one(article)
            return {
                "title": article["title"],
                "nanoId": article["nanoId"],
                "publishTime": currentDateTime.isoformat(),
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
            for i in mongo.db.articles.find().sort("publishDateTime", -1)[
                offset : offset + PAGE_SIZE
            ]
        ]


@article.route("/article/single/<string:nanoId>")
class SingleArticle(MethodView):
    @article.response(200, SingleArticleSchema)
    def get(this, nanoId):
        data = {"article": mongo.db.articles.find_one({"nanoId": nanoId})}
        prev = (
            mongo.db.articles.find({"_id": {"$gt": data["article"]["_id"]}})
            .sort("_id", -1)
            .limit(1)
        )
        next = (
            mongo.db.articles.find({"_id": {"$gt": data["article"]["_id"]}})
            .sort("_id")
            .limit(1)
        )
        print(prev)
        print(next)

        if prev[0] is not None:
            data["prevNanoId"] = prev[0]["nanoId"]
            data["prevTitle"] = prev[0]["title"]
        if next[0] is not None:
            data["nextNanoId"] = next[0]["nanoId"]
            data["nextTitle"] = next[0]["title"]

        return data


@article.route("/article/pageCount")
class PageCount(MethodView):
    @article.response(200, PageCountSchema)
    def get(this):
        return {
            "pageCount": math.ceil(mongo.db.articles.count_documents({}) / PAGE_SIZE)
        }
