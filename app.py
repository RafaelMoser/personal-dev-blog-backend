"""
app.py

flask app
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from dotenv import dotenv_values
from flask_jwt_extended import JWTManager

from db import mongo
from blocklist import BLOCKLIST

from resources.blog_articles import article
from resources.blog_info import blogInfo

dotEnv = dotenv_values()


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
    app.config["MONGO_URI"] = dotEnv["MONGODB_URI"]
    app.config["JWT_SECRET_KEY"] = dotEnv["JWT_SECRET_KEY"]

    mongo.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_jwt_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return jsonify({"message":"The token has been revoked.","error":"token_revoked"}),401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return jsonify({"message":"The token has expired.","error":"token_expired"}),401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"Signature verification failed.","error":"invalid_token"}),401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message":"Request does not contain an access token.","error":"authorization_required"}),401

    api.register_blueprint(article)
    api.register_blueprint(blogInfo)

    return app
