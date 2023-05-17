"""
db.py

database operations
"""

from flask_pymongo import PyMongo

mongo = PyMongo()

page_size = -1

def get_page_size():
    if page_size == -1:
        page_size = mongo.db.blogconfig.find_one()["pageSize"]
    return page_size

def generate_nanoId():
    nanoId = generate(size=6)
    while mongo.db.articles.count_documents({"nanoId": nanoId}) != 0:
        nanoId = generate(size=6)
    return nanoId

def get_blog_info():
    return mongo.db.bloginfo.find_one()

def update_blog_info(update_data):
    mongo.db.bloginfo.update_one({}, update_data)

def insert_article(article):
    mongo.db.articles.insert_one(article)

def update_article(article):
    mongo.db.articles.update_one({"nanoId":article["nanoId"]}, article)

def get_article(nanoId):
    return mongo.db.articles.find_one({"nanoId": nanoId})

def delete_article(nanoId):
    mongo.db.articles.delete_one({"nanoId":nanoId})

def get_article_count()
    return mongo.db.articles.count_documents({})

def get_article_page(page):
    offset = (page - 1) * get_page_size()
    return [i for i in mongo.db.articles.find().sort("publishDateTime", -1)[offset : offset + get_page_size()]]

def get_adjacent_articles_nanoId_title(article):
    prev = list(
        mongo.db.articles.find({"_id": {"$lt": article["_id"]}})
        .sort([("_id", -1)])
        .limit(1)
    )
    next = list(
        mongo.db.articles.find({"_id": {"$gt": article["_id"]}})
        .sort("_id")
        .limit(1)
    )
    data=dict()
    if len(prev) != 0:
        data["prevNanoId"] = prev[0]["nanoId"]
        data["prevTitle"] = prev[0]["title"]
    if len(next) != 0:
        data["nextNanoId"] = next[0]["nanoId"]
        data["nextTitle"] = next[0]["title"]
    return data

def get_user_data(user_data):
    return mongo.db.users.find_one({"username": user_data["username"]})