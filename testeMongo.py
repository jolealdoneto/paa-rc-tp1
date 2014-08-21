from pymongo import MongoClient
import datetime
import json

client = MongoClient()
db = client.test_database

posts = db.posts
post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"], "date": datetime.datetime.utcnow()}
post_id = posts.insert(post)
print(post_id)
