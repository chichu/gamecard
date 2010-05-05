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
#from gamecard.logging import *
from forms import *

MAX_CHANCE_CARD_IDS = 5
MAX_NOTICE = 5
MAX_ANOUNCE = 3

def get_card(request,item_id):
    #if not request.COOKIES.has_key('user_name'):
    #    return render_to_response('card/popups/login.html')
        
    if request.COOKIES.has_key("has_get"):
        return render_to_response('card/popups/failure2.html')
 
    if request.method == "POST":
        username = request.COOKIES.get('user_name')
        item = Item.objects.get(id=item_id)
        
        #input_code = request.POST.get("checkcode","")
        #if input_code.strip() != request.session['checkcode']:
            #return render_to_response('card/popups/get_notice.html',{'item_id':item_id,'error':u'验证码输入错误！'})
        '''
        1.get one available card for user 
        2.change the info of the card
        '''
        try:
            collect = get_mongodb_collect(get_collect_name(item_id))
            avail_one = collect.find_one({"status":"normal"})
            if not bool(avail_one):
                return render_to_response('card/popups/failure3.html',{'item':item})
            
            card_id = avail_one['card_id'] 
            avail_one = tag_used_card(username,item,avail_one)
            collect.save(avail_one)
        except Exception,e:
            log_error("Failed in getting one card and saving the info:%s %s %s"%(e,username,item))
            return render_to_response('card/popups/get_notice.html',{'item_id':item_id,'error':'领卡错误！'})
        '''
        save the card in user's cards inbox
        '''    
        error = save_user_card_id(username,item,card_id)
        if bool(error):
            log_error("Failed in saving user card id%s %s %s"%(error,username,item))
        '''
        set the cookie to note that this user has get one card,and can not get any in 24 hours
        '''
        res = render_to_response('card/popups/get_success.html',{'item':item,"card_id":card_id})
        res.set_cookie(key='has_get', value=True, max_age=SESSION_COOKIE_AGE, domain=SESSION_COOKIE_DOMAIN)
        return res
    return render_to_response('card/popups/get_notice.html',{'item_id':item_id})   
        
       
def get_chance(request,item_id):
    if request.method == "POST":
        try:
            item = Item.objects.get(id=item_id)
            if item.is_chance == False:
                return render_to_response('card/popups/no_chance_available.html')
            collect = get_mongodb_collect(get_collect_name(item_id))
            conditions = {'status':"used","chance_time":{"$lt": datetime.now()}}
            avails = collect.find(conditions).sort("count").limit(MAX_CHANCE_CARD_IDS)
            if avails.count() < MAX_CHANCE_CARD_IDS:
                return render_to_response('card/popups/no_chance_card.html')
            for one in avails:
                one['count'] += 1
                chance_collect.save(one)
        except:
            return render_to_response('card/popups/chance_notice.html',{'item':item,'error':'领卡错误！'})
        return render_to_response('card/popups/chance_success.html',{'item':item})
    return render_to_response('card/popups/chance_notice.html',{'item_id':item_id})   
      
      
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
    return render_to_response('card/i2.html',{"activity":Activity.objects.get(id=activity_id)})
    
    
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
