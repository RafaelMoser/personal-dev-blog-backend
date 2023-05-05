from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("articles", __name__, description="Article fetcher")


@blp.route("/article/list/<integer:page>")
class ArticleListPageFetcher:
    def get(this, page):
        pass


@blp.route("/article/<string:article_id>")
class SingleArticleFetcher(MethodView):
    def get(this, article_id):
        pass
