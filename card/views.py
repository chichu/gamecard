#encoding:utf-8
# Create your views here.
from django.utils.encoding import smart_unicode,force_unicode,smart_str
from django.views.decorators.cache import cache_page
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *
from datetime import datetime,timedelta
from gamecard.utils.dbutils import *
from gamecard.utils.strutils import *
from gamecard.settings import *
from gamecard.log import *
from forms import *

def get_card(request,item_id):
    if not request.session.test_cookie_worked():
        print "cookie unenabled!" 

    #if not request.COOKIES.has_key('user_name'):
    #    return render_to_response('card/popups/login.html')
    if request.COOKIES.has_key("has_get"):
        return render_to_response('card/popups/failure2.html',{'item_id':item_id})
 
    if request.method == "POST":
        username = request.COOKIES.get('user_name','chichu')
        item = Item.objects.get(id=item_id)
        
        input_code = request.POST.get("checkcode","").strip()
        checkcode = request.session.get('checkcode','error')
        if input_code != checkcode:
        	return render_to_response('card/popups/get_notice.html',{'item_id':item_id,'error':u'验证码输入错误！'})
        '''
        1.get one available card for user 
        2.change the info of the card
        '''
        try:
            collect = get_mongodb_collect(get_collect_name(item_id))
            avail_one = collect.find_one({"status":"normal"})
            if not bool(avail_one):
                return render_to_response('card/popups/failure3.html',{'item_id':item_id})
            
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
        #res.set_cookie(key='has_get', value=True, max_age=SESSION_COOKIE_AGE, domain=SESSION_COOKIE_DOMAIN)
        return res
    return render_to_response('card/popups/get_notice.html',{'item_id':item_id})   
        
MAX_CHANCE_CARD_IDS = 5   
def get_chance(request,item_id):
    if request.method == "POST":
        try:
            item = Item.objects.get(id=item_id)
            input_code = request.POST.get("checkcode","").strip()
            checkcode = request.session.get('checkcode','error')
            if input_code != checkcode:
            	return render_to_response('card/popups/chance_notice.html',{'item_id':item_id,'error':u'验证码输入错误！'})
            if item.is_chance == False:
                return render_to_response('card/popups/chance_not_available.html')
            collect = get_mongodb_collect(get_collect_name(item_id))
            conditions = {'status':"used","chance_time":{"$lt": datetime.now()}}
            avails = collect.find(conditions).sort("count").limit(MAX_CHANCE_CARD_IDS)
            if avails.count() < MAX_CHANCE_CARD_IDS:
                return render_to_response('card/popups/no_chance_card.html')
            card_ids = ",".join([one['card_id'] for one in avails]) 
            for one in avails:
                one['count'] += 1
                collect.save(one)
        except Exception,e:
            log_error("error in get chance %s" % e)
            return render_to_response('card/popups/chance_notice.html',{'item_id':item_id,'error':"error!"})
        return render_to_response('card/popups/chance_success.html',{'item':item,'card_ids':card_ids})
    return render_to_response('card/popups/chance_notice.html',{'item_id':item_id})   
      
def index(request):
    username = ''
    return render_to_response('card/index.html',locals())

def coperation(request):
    return render_to_response('card/coperation.html',locals())
    
def activity_detail(request,activity_id):
    online_news = OnlineNews.objects.all().order_by('-online_time')[0:MAX_NOTICE]
    activity = Activity.objects.get(id=activity_id)
    return render_to_response('card/i2.html',locals())
    
def item_detail(request):
    card_id = request.GET.get('card_id','')
    item_id = request.GET.get('item_id','')
    item = Item.objects.get(id=item_id)
    return render_to_response('card/popups/item_details.html',locals())
    
CHECKCODE_IMAGE_PATH = os.path.join(MEDIA_ROOT,'images/checkcode.gif')
FONT_PATH =  os.path.join(MEDIA_ROOT,"simhei.ttf")
def get_check_code_image(request,image=CHECKCODE_IMAGE_PATH):
    import Image, ImageDraw, ImageFont, random, md5,cStringIO 
    try:
    	im = Image.open(image)  
    	draw = ImageDraw.Draw(im)  
    	mp = md5.new()  
    	mp_src = mp.update(str(datetime.now()))  
    	mp_src = mp.hexdigest()  
    	rand_str = mp_src[0:4]     
    	draw.text((15,0), rand_str[0], font=ImageFont.truetype(FONT_PATH, random.randrange(15,25)))  
    	draw.text((30,0), rand_str[1], font=ImageFont.truetype(FONT_PATH, random.randrange(15,25)))  
    	draw.text((45,0), rand_str[2], font=ImageFont.truetype(FONT_PATH, random.randrange(15,25)))  
    	draw.text((60,0), rand_str[3], font=ImageFont.truetype(FONT_PATH, random.randrange(15,25)))  
    	del draw
    	request.session['checkcode'] = rand_str  
    	buf = cStringIO.StringIO()  
    	im.save(buf, 'gif')  
    except Exception,e:
    	log_error("%s:%s"%("Error in generate checkcode",e))
    	print e
    return HttpResponse(buf.getvalue(),'image/gif') 

