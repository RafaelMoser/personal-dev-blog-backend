from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from dotenv import dotenv_values

from db import mongo

from resources.blog_articles import article
from resources.personal_info import personalInfo

config = dotenv_values()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Personal Dev Blog API"
    app.config["API_VERSION"] = "v0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["MONGO_URI"] = config["MONGODB_URI"]

    mongo.init_app(app)

    api = Api(app)
    api.register_blueprint(article)
    api.register_blueprint(personalInfo)

    return app
