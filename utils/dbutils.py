#encoding:utf-8
from pymongo import Connection,ASCENDING

MONGODB_NAME = "gamecard"
MONGODB_HOST = "localhost"
MONGODB_PORT = 0
MONGODB_PASSWORD = "password"

def get_mongodb_cursor(collection,database=MONGODB_NAME):
    db = Connection()[database]
    cursor = db[collection]
    return cursor
