from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import ArticleSchema

blp = Blueprint("articles", __name__, description="Article fetcher")


@blp.route("/article/list/<integer:page>")
class ArticleListPage(MethodView):
    @blp.response(200, ArticleSchema(many=True))
    def get(this, page):
        pass


@blp.route("/article/<string:article_id>")
class SingleArticle(MethodView):
    @blp.response(200, ArticleSchema)
    def get(this, article_id):
        pass
    
    @blp.response(200, ArticleSchema)
    def post(this):
        pass
