#encoding:utf-8
from strutils import *

MONGODB_NAME = "gamecard"
MONGODB_HOST = "localhost"
MONGODB_PORT = 0
MONGODB_PASSWORD = "password"

def get_mongodb_cursor(collection,database=MONGODB_NAME,index=None):
    from pymongo import Connection
    db = Connection()[database]
    cursor = db[collection]
    if not bool(index):
        cursor.create_index([(index, ASCENDING)])
    return cursor

def insert_card_ids(all_lines,item):
    collect_name = get_collect_name(item.id)
    cursor =  get_mongodb_cursor(collect_name,"status")
    insert_items = []
    for line in all_lines:
        inserts = get_cardfile_dict(item.format,line)
        for insert in inserts:
            insert_items.append(insert)
    try:
        cursor.insert(insert_items)
        return len(insert_items)
    except Exception,e:
        print e
        return 0
    