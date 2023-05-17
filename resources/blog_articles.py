"""
blog_articles.py

article related API endpoints
"""

from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from schemas import ArticleSchema, PageCountSchema, SingleArticleSchema
from datetime import datetime
from nanoid import generate
import math

import db

article = Blueprint("articles", __name__, description="Articles")

@article.route("/article/new")
class PublishArticle(MethodView):
    @jwt_required()
    @article.arguments(NewArticleSchema)
    @article.response(201, ArticleSchema)
    def post(self, article_data):
        nanoId = db.generate_nanoId()
        currentDateTime = datetime.now()
        newArticle = {
            "title": article_data.title,
            "articleBody": article_data.articleBody,
            "publishDateTime": currentDateTime,
            "nanoId": nanoId,
        }
        try:
            db.insert_article(article)
            return newArticle
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400


@article.route("/article/list/<int:page>")
class ArticleListPage(MethodView):
    @article.response(200, ArticleSchema(many=True))
    def get(self, page):
        return db.get_article_page(page)


@article.route("/article/single/<string:nanoId>")
class SingleArticle(MethodView):
    @article.response(200, SingleArticleSchema)
    def get(self, nanoId):
        article = db_get_article(nanoId)
        data = db.get_adjacent_nanoId_title(article)
        data["article"] = article
        return data

    @jwt_required()
    @article.arguments(ArticleSchema)
    @article.response(201,ArticleSchema)
    def patch(self, article_data):
        article_data["lastUpdateDateIme"] = datetime.now()
        try:
            db.update_article(article_data)
            return article_data
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400
    
    @jwt_required(fresh=True)
    @article.response(201,ArticleSchema)
    def delete(self, nanoId):
        try:
            article = db.get_article(nanoId)
            db.delete_article(nanoId)
            return article
        except Exception as error:
            print(error)
            return jsonify({"error": error.__str__}),400


@article.route("/article/pageCount")
class PageCount(MethodView):
    @article.response(200, PageCountSchema)
    def get(self):
        return {
            "pageCount": math.ceil(db.get_article_count() / db.get_page_size())
        }
