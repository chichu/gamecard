#encoding:utf-8
# Create your views here.
from models import *
from datetime import datetime
from gamecard.utils.dbutil import *
from gamecard.utils.strutil import *

CHANGE_IDS_PERTIME = 3

def get_card(request):
    if request.method == "GET":
        item_id = request.GET.['item_id']
        username = request.COOKIES['user_name']
        if request.COOKIES.has_key("has_get"):
            return "你已经领取过一次"
            
        item = Item.objects.get(id=item_id)
        collect_name = get_collect_name(item_id)
        cursor = get_mongodb_cursor(collect_name)
        
        avail_one = cursor.find_one({"status":"normal"})
        avail_one["username"] = username
        avail_one["status"] = "used"
        avail_one["get_time"] = datetime.now()
        if item.is_chance:
            avail_one['is_chance'] = True
            avail_one["count"] = 0
            avail_one["chance_time"] = item.chance_time
        request.COOKIES.set_cookies('has_get',True,expire=24*3600)
        return render_to_response('',)
       

def get_chance(request):
    if request.method == "GET":
        item_id = request.GET['item_id']

        item = Item.objects.get(id=item_id)
        collect_name = get_collect_name(item_id)
        cursor = get_mongodb_cursor(collect_name)
        conditions = {'status':"used",'is_change':True,"chance_time":{"$lt": datetime.now()}}
        avails = chance_cursor.find(conditions,limit=MAX_CHANCE_CARD_IDS).order_by('count')
        if avails.count() < CHANGE_IDS_PERTIME:
            return "not enough chance ids"
        for one in avails:
            one['count'] += 1
            chance_cursor.save(one)
        return avails
        
        
    
    
