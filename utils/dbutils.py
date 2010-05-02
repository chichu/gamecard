#encoding:utf-8
from pymongo import Connection,ASCENDING

MONGODB_NAME = "gamecard"
MONGODB_HOST = "localhost"
MONGODB_PORT = 0
MONGODB_PASSWORD = "password"

def get_mongodb_collect(collection,database=MONGODB_NAME):
    db = Connection()[database]
    collect = db[collection]
    return collect
