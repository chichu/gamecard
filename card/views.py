#encoding:utf-8
# Create your views here.
from django.utils.encoding import smart_unicode,force_unicode,smart_str
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *
from datetime import datetime,timedelta
from gamecard.utils.dbutils import *
from gamecard.utils.strutils import *

CHANGE_IDS_PERTIME = 5

def get_card(request):
    if request.method == "POST":
        item_id = request.GET.get('item_id',1)
        username = request.COOKIES.get('user_name','chichu')
        if request.COOKIES.has_key("has_get"):
            return render_to_response('card/popup/failure2.html',{'item':item})
        item = Item.objects.get(id=item_id)
        collect_name = get_collect_name(item_id)
        cursor = get_mongodb_cursor(collect_name)
        #find a available one
        avail_one = cursor.find_one({"status":"normal"})
        if not bool(avail_one):
            return render_to_response('card/popup/failure3.html',{'item':item})
            
        avail_one["username"] = username
        avail_one["status"] = "used"
        avail_one["get_time"] = datetime.now()
        if item.is_chance:
            avail_one['is_chance'] = True
            avail_one["count"] = 0
            avail_one["chance_time"] = datetime.now()+timedelta(hours=int(item.chance_time_delta))
        avail_one.save()
        #save user info
        cursor = get_mongodb_cursor("user_info",indexs=[('name',True)])
        user = cursor.find_one({"name":username})
        if bool(user):
            user['cards'] += {'item_id':item_id,'card_id':avail_one['card_id']}
            user.save()
        else:
            new_user = {"name":username,'cards':[{'item_id':item_id,'card_id':avail_one['card_id']}]}
            cursor.insert(new_user)
        request.COOKIES.set_cookies('has_get',True,expire=24*3600)
        return render_to_response('card/popup/get_success.html',{'item':item})
    return render_to_response('card/popup/get_notice.html',{'item':item})
       

def get_chance(request):
    if request.method == "POST":
        item_id = request.GET['item_id']

        item = Item.objects.get(id=item_id)
        collect_name = get_collect_name(item_id)
        cursor = get_mongodb_cursor(collect_name)
        conditions = {'status':"used",'is_change':True,"chance_time":{"$lt": datetime.now()}}
        avails = chance_cursor.find(conditions,limit=MAX_CHANCE_CARD_IDS).order_by('count')
        if avails.count() < CHANGE_IDS_PERTIME:
            return render_to_response('card/popup/failure4.html',{'item':item})
        for one in avails:
            one['count'] += 1
            chance_cursor.save(one)
        return render_to_response('card/popup/chance_success.html',{'item':item})
    return render_to_response('card/popup/chance_notice.html',{'item':item})   
      
def index(request):
    begin_cards = None       
    return render_to_response('card/index.html',locals())
   
def detail(request): 
    return render_to_response('card/i2.html',locals())
