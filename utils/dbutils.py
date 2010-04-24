#encoding:utf-8
from strutils import *
from pymongo import Connection,ASCENDING

MONGODB_NAME = "gamecard"
MONGODB_HOST = "localhost"
MONGODB_PORT = 0
MONGODB_PASSWORD = "password"

def get_mongodb_cursor(collection,database=MONGODB_NAME,indexs=[]):
    db = Connection()[database]
    cursor = db[collection]
    if bool(indexs):
        for index,is_unique in indexs: 
             cursor.create_index(index,unique=is_unique)
    return cursor

def insert_card_ids(all_lines,item):
    collect_name = get_collect_name(item.id)
    indexs=[("status",False)]
    if item.format.find("count") == -1:
        indexs.append(("card_id",True))
    cursor =  get_mongodb_cursor(collect_name,indexs=indexs)
    for line in all_lines:
        inserts = get_cardfile_dict(item.format,line)
        try:
            for insert in inserts:
                cursor.insert(insert)
        except Exception,e:
            continue 
    curosr.commit()
    return cursor.count()
