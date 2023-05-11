from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.String(dump_only=True)
    nanoId = fields.String(dump_only=True)
    title = fields.String(required=True)
    publishDate = fields.String(required=True)
    publishTime = fields.String(required=True)
    articleBody = fields.String(required=True)


class PageCountSchema(Schema):
    pageCount = fields.Number(required=True)


class SingleArticleSchema(Schema):
    article = fields.Nested(lambda: ArticleSchema(), required=True)
    prev = fields.String()
    next = fields.String()
