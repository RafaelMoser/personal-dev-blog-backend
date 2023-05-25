"""
db.py

database operations
"""

from flask_pymongo import PyMongo
from nanoid import generate

mongo = PyMongo()

page_size = -1

# Article related db calls


def get_page_size():
    global page_size
    if page_size == -1:
        page_size = mongo.db.blogconfig.find_one()["pageSize"]
    return page_size


def generate_nanoId():
    nanoId = generate(size=6)
    while mongo.db.articles.count_documents({"nanoId": nanoId}) != 0:
        nanoId = generate(size=6)
    return nanoId


def insert_article(article):
    mongo.db.articles.insert_one(article)


def update_article(article, nanoId):
    new_values = {
        "$set": {
            "title": article["title"],
            "articleBody": article["articleBody"],
            "lastUpdateDateTime": article["lastUpdateDateTime"],
        }
    }
    mongo.db.articles.update_one({"nanoId": nanoId}, new_values)


def get_article(nanoId):
    return mongo.db.articles.find_one({"nanoId": nanoId})


def delete_article(nanoId):
    mongo.db.articles.delete_one({"nanoId": nanoId})


def get_article_count():
    return mongo.db.articles.count_documents({})


def get_article_page(page):
    offset = (page - 1) * get_page_size()
    return [
        i
        for i in mongo.db.articles.find().sort("publishDateTime", -1)[
            offset : offset + get_page_size()
        ]
    ]


def get_adjacent_articles_nanoId_title(article):
    prev = list(
        mongo.db.articles.find({"_id": {"$lt": article["_id"]}})
        .sort([("_id", -1)])
        .limit(1)
    )
    next = list(
        mongo.db.articles.find({"_id": {"$gt": article["_id"]}}).sort("_id").limit(1)
    )
    data = dict()
    if len(prev) != 0:
        data["prevNanoId"] = prev[0]["nanoId"]
        data["prevTitle"] = prev[0]["title"]
    if len(next) != 0:
        data["nextNanoId"] = next[0]["nanoId"]
        data["nextTitle"] = next[0]["title"]
    return data


# Blog info related db calls


def get_full_blog_info():
    return mongo.db.bloginfo.find_one({})


def get_blog_info():
    return mongo.db.bloginfo.find_one(
        {},
        {
            "_id": 0,
            "profileImageUrl": 1,
            "infoBlurb": 1,
            "github": 1,
            "linkedin": 1,
            "email": 1,
        },
    )


def replace_blog_info(update_data):
    mongo.db.bloginfo.replace_one({}, update_data)


def get_about_me():
    return mongo.db.bloginfo.find_one({}, {"_id": 0, "aboutMe": 1})


def get_blog_name():
    return mongo.db.bloginfo.find_one({}, {"_id": 0, "blogName": 1})


# Login related db calls


def get_user_data(user_data):
    return mongo.db.users.find_one({"username": user_data["username"]})


def register_user(user_data):
    return mongo.db.users.insert_one(
        {"username": user_data["username"], "password": user_data["password"]}
    )


def user_exists(username):
    return mongo.db.users.count_documents({"username": username}) != 0
