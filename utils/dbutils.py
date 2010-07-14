#encoding:utf-8
from pymongo import Connection,ASCENDING
from datetime import datetime,timedelta
from gamecard.settings import DEBUG

MONGODB_NAME = "gamecard"
MONGODB_HOST = "localhost"
MONGODB_PORT = 0
MONGODB_PASSWORD = "password"
if DEBUG:
    MONGODB_NAME = "gamecard_test"
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 0
    MONGODB_PASSWORD = "password"

USER_INFO = "user_info"
CARD_AUDIT_INFO = "card_audit_info"

def get_mongodb_collect(collection,database=MONGODB_NAME):
    db = Connection()[database]
    collect = db[collection]
    return collect
    
def save_user_card_id(username,item,object_id):
    collect = get_mongodb_collect(USER_INFO)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        if collect.ensure_index("name"): 
            collect.create_index('name',unique=True)
        user = collect.find_one({"name":username})
        if bool(user):
            user['cards'].append((item.name,item.id,object_id,timestamp))
            collect.save(user)
        else:
            new_user = {"name":username,'cards':[(item.name,item.id,object_id,timestamp)]}
            collect.insert(new_user)
    except Exception,e:
        print e
        return e
    return None
    
def tag_used_card(username,item,avail_one):
    now = datetime.now()
    avail_one["username"] = username
    avail_one["status"] = "used"
    avail_one["get_time"] = now
    if item.is_chance:
        avail_one["count"] = 0
        avail_one["chance_time"] = now+timedelta(hours=int(item.chance_time_delta))
    return avail_one
    

def set_count(name,item_id):
    from django.core.cache import cache
    try:
        key = "%s_%s"%(name,item_id)
        tmp = cache.get(key,0)
        tmp += 1
        cache.set(key,tmp,3600*24)
    except Exception,e:
        print e
        return False
    return True
    
def get_count(name,item_id):
    from django.core.cache import cache
    key = "%s_%s"%(name,item_id)
    tmp = cache.get(key,0)
    return tmp 
    