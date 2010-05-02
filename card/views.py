#encoding:utf-8
# Create your views here.
from django.utils.encoding import smart_unicode,force_unicode,smart_str
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *
from datetime import datetime,timedelta
from gamecard.utils.dbutils import *
from gamecard.utils.strutils import *
from gamecard.settings import *
from forms import *
CHANGE_IDS_PERTIME = 5
MAX_NOTICE = 5
MAX_ANOUNCE = 3

def get_card(request,item_id):
    item = Item.objects.get(id=item_id)
    if request.method == "POST":
        username = request.COOKIES.get('user_name','chichu')
        #input_code = request.POST.get("checkcode","")
        #if input_code.strip() != request.session['checkcode']:
        #    return HttpResponse("<script>alert('thanks');</script>")
            #return render_to_response('card/popups/get_notice.html',{'item':item})
        
        collect_name = get_collect_name(item_id)
        collect = get_mongodb_collect(collect_name)
        #find a available one
        avail_one = collect.find_one({"status":"normal"})
        if not bool(avail_one):
            return render_to_response('card/popups/failure3.html',{'item':item})
            
        avail_one["username"] = username
        avail_one["status"] = "used"
        avail_one["get_time"] = datetime.now()
        if item.is_chance:
            avail_one['is_chance'] = True
            avail_one["count"] = 0
            avail_one["chance_time"] = datetime.now()+timedelta(hours=int(item.chance_time_delta))
        collect.save(avail_one)
        #save user info
        collect = get_mongodb_collect("user_info")
        if collect.ensure_index("name"): 
            collect.create_index('name',unique=True)
        user = collect.find_one({"name":username})
        if bool(user):
            user['cards'] += {'item_id':item_id,'card_id':avail_one['card_id']}
            collect.save(user)
        else:
            new_user = {"name":username,'cards':[{'item_id':item_id,'card_id':avail_one['card_id']}]}
            collect.insert(new_user)
        res = render_to_response('card/popups/get_success.html',{'user_info':collect.find_one({"name":username}),'item':item,"card_id":avail_one['card_id']})
        res.set_cookie(key='has_get', value=True, max_age=SESSION_COOKIE_AGE, domain=SESSION_COOKIE_DOMAIN)
        return res
    else:
        username = request.COOKIES.get('user_name','chichu')
        if not bool(username):
            return render_to_response('card/popups/login.html')
        if request.COOKIES.has_key("has_get"):
            return render_to_response('card/popups/failure2.html')
        return render_to_response('card/popups/get_notice.html',{'item':item})
       

def get_chance(request,item_id):
    item = Item.objects.get(id=item_id)
    if request.method == "POST":
        collect_name = get_collect_name(item_id)
        collect = get_mongodb_collect(collect_name)
        conditions = {'status':"used",'is_change':True,"chance_time":{"$lt": datetime.now()}}
        avails = chance_collect.find(conditions,limit=MAX_CHANCE_CARD_IDS).order_by('count')
        if avails.count() < CHANGE_IDS_PERTIME:
            return render_to_response('card/popups/failure4.html',{'item':item})
        for one in avails:
            one['count'] += 1
            chance_collect.save(one)
        return render_to_response('card/popups/chance_success.html',{'item':item})
    return render_to_response('card/popups/chance_notice.html',{'item':item})   
      
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
    
def get_check_code_image(request,image='/tmp/checkcode.gif'):
    import Image, ImageDraw, ImageFont, random
    from gamecard.settings import MEDIA_ROOT
    font_path = os.path.join(MEDIA_ROOT,'ukai.ttf')
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    mp = md5.new()
    mp_src = mp.update(str(datetime.now()))
    mp_src = mp.hexdigest()
    rand_str = mp_src[0:4]   
    draw.text((10,10), rand_str[0], font=ImageFont.truetype(font_path, random.randrange(25,50)))
    draw.text((48,10), rand_str[1], font=ImageFont.truetype(font_path, random.randrange(25,50)))
    draw.text((85,10), rand_str[2], font=ImageFont.truetype(font_path, random.randrange(25,50)))
    draw.text((120,10), rand_str[3], font=ImageFont.truetype(font_path, random.randrange(25,50)))
    del draw
    request.session['checkcode'] = rand_str
    buf = cStringIO.StringIO()
    im.save(buf, 'gif')
    return HttpResponse(buf.getvalue(),'image/gif')
