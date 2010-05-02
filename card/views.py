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
MAX_NOTICE = 5
MAX_ANOUNCE = 3

def get_card(request,item_id):
    if request.method == "POST":
        item = Item.objects.get(id=item_id)
        collect_name = get_collect_name(item_id)
        collect = get_mongodb_collect(collect_name)
        #find a available one
        avail_one = collect.find_one({"status":"normal"})
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
        collect = get_mongodb_collect("user_info",indexs=[('name',True)])
        user = collect.find_one({"name":username})
        if bool(user):
            user['cards'] += {'item_id':item_id,'card_id':avail_one['card_id']}
            user.save()
        else:
            new_user = {"name":username,'cards':[{'item_id':item_id,'card_id':avail_one['card_id']}]}
            collect.insert(new_user)
        request.COOKIES.set_cookies('has_get',True,expire=24*3600)
        return render_to_response('card/popup/get_success.html',{'item':item})
    else:
        username = request.COOKIES.get('user_name')#,'chichu')
        if not bool(username):
            return render_to_response('card/popup/login.html')
        if request.COOKIES.has_key("has_get"):
            return render_to_response('card/popup/failure2.html')
        return render_to_response('card/popup/get_notice.html')
       

def get_chance(request,item_id):
    item = Item.objects.get(id=item_id)
    if request.method == "POST":
        collect_name = get_collect_name(item_id)
        collect = get_mongodb_collect(collect_name)
        conditions = {'status':"used",'is_change':True,"chance_time":{"$lt": datetime.now()}}
        avails = chance_collect.find(conditions,limit=MAX_CHANCE_CARD_IDS).order_by('count')
        if avails.count() < CHANGE_IDS_PERTIME:
            return render_to_response('card/popup/failure4.html',{'item':item})
        for one in avails:
            one['count'] += 1
            chance_collect.save(one)
        return render_to_response('card/popup/chance_success.html',{'item':item})
    return render_to_response('card/popup/chance_notice.html',{'item':item})   
      
def index(request):
    anounces = Anounce.objects.all().order_by('-create_time')[0:MAX_ANOUNCE]
    notices = Notice.objects.all().order_by('-create_time')[0:MAX_NOTICE]
    pictures = Pictures.objects.filter(is_active=True).order_by('-create_time')
    
    begin_cards = Activity.objects.filter(card_type='begin_card',status="active")
    act_codes = Activity.objects.filter(card_type='act_code',status="active")
    
    (b_hot,b_new,b_alpha) = get_ordered_act(act_codes,start_alpha_index=2)
    (a_hot,a_new,a_alpha) = get_ordered_act(begin_cards,start_alpha_index=12)    
    return render_to_response('card/index.html',locals())
    
def activity_detail(request,activity_id): 
    activity = Activity.objects.get(id=activity_id)
    content = activity.info
    return render_to_response('card/i2.html',locals())
