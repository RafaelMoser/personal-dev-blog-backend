from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    publishDate = fields.Date(required=True)
    articleBody = fields.String(required=True)
