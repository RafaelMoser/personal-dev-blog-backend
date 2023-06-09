"""
schemas.py

schemas for API request filtering
"""

from marshmallow import Schema, fields


class BlogInfoSchema(Schema):
    profileImageUrl = fields.String(required=True)
    infoBlurb = fields.String(required=True)
    github = fields.String()
    linkedin = fields.String()
    email = fields.String()


class BlogNameSchema(Schema):
    blogName = fields.String(required=True)


class AboutMeSchema(Schema):
    aboutMe = fields.String(required=True)


class BlogInfoUpdateSchema(Schema):
    id = fields.String(dump_only=True)
    profileImageUrl = fields.String(required=True)
    infoBlurb = fields.String(required=True)
    aboutMe = fields.String(required=True)
    github = fields.String()
    linkedin = fields.String()
    email = fields.Email()


class NewArticleSchema(Schema):
    title = fields.String(required=True)
    articleBody = fields.String(required=True)


class ArticleSchema(Schema):
    id = fields.String(dump_only=True)
    nanoId = fields.String(dump_only=True, unique=True)
    title = fields.String(required=True)
    publishDateTime = fields.DateTime(required=True)
    lastUpdateDateTime = fields.DateTime()
    articleBody = fields.String(required=True)


class UpdateArticleSchema(Schema):
    title = fields.String(required=True)
    articleBody = fields.String(required=True)


class PageCountSchema(Schema):
    pageCount = fields.Number(required=True)


class SingleArticleSchema(Schema):
    article = fields.Nested(lambda: ArticleSchema(), required=True)
    prevNanoId = fields.String()
    prevTitle = fields.String()
    nextNanoId = fields.String()
    nextTitle = fields.String()


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True, unique=True)
    password = fields.String(required=True, load_only=True)
