from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from schemas import ArticleSchema, PageCountSchema, SingleArticleSchema
from datetime import datetime
from nanoid import generate
import math

from db import mongo

PAGE_SIZE = 3
article = Blueprint("articles", __name__, description="Articles")


@article.route("/article/new")
class PublishArticle(MethodView):
    @jwt_required()
    @article.arguments(NewArticleSchema)
    @article.response(201, ArticleSchema)
    def post(self, article_data):
        nanoId = generate(size=6)
        while mongo.db.articles.count_documents({"nanoId": nanoId}) != 0:
            nanoId = generate(size=6)
        currentDateTime = datetime.now()
        newArticle = {
            "title": article_data.title,
            "articleBody": article_data.articleBody,
            "publishDateTime": currentDateTime,
            "nanoId": nanoId,
        }
        try:
            mongo.db.articles.insert_one(article)
            return newArticle
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400


@article.route("/article/list/<int:page>")
class ArticleListPage(MethodView):
    @article.response(200, ArticleSchema(many=True))
    def get(self, page):
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
    def get(self, nanoId):
        data = {"article": mongo.db.articles.find_one({"nanoId": nanoId})}
        prev = list(
            mongo.db.articles.find({"_id": {"$lt": data["article"]["_id"]}})
            .sort([("_id", -1)])
            .limit(1)
        )
        next = list(
            mongo.db.articles.find({"_id": {"$gt": data["article"]["_id"]}})
            .sort("_id")
            .limit(1)
        )

        if len(prev) != 0:
            data["prevNanoId"] = prev[0]["nanoId"]
            data["prevTitle"] = prev[0]["title"]
        if len(next) != 0:
            data["nextNanoId"] = next[0]["nanoId"]
            data["nextTitle"] = next[0]["title"]
        return data

    @jwt_required()
    @article.arguments(ArticleSchema)
    @article.response(201,ArticleSchema)
    def patch(self, article_data):
        article_data["lastUpdateDateIme"] = datetime.now()
        try:
            mongo.db.articles.update_one({"nanoId":article["nanoId"],article)
            return article_data
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400
    
    @jwt_required()
    @article.response(201,ArticleSchema)
    def delete(self, nanoId):
        try:
            article = mongo.db.articles.find_one({"nanoId": nanoId})
            mongo.db.articles.delete_one({"nanoId":nanoId})
            return article
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400


@article.route("/article/pageCount")
class PageCount(MethodView):
    @article.response(200, PageCountSchema)
    def get(self):
        return {
            "pageCount": math.ceil(mongo.db.articles.count_documents({}) / PAGE_SIZE)
        }
