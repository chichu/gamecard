# encoding: utf-8
from django import template
from gamecard.card.models import *

register = template.Library()

MAX_NOTICE = 5
MAX_ANOUNCE = 3

@register.inclusion_tag('card/headnav.html')
def headnav(nav_index,username):
    return {
        'username':username,
        'nav_index' : nav_index,
    }
    
@register.inclusion_tag('card/side.html')
def sidebar():
    online_news = OnlineNews.objects.all().order_by('-online_time')[0:MAX_NOTICE*3]
    return {
        'online_news':online_news,
    }

@register.inclusion_tag('card/login_info.html')
def logininfobar(username):
    return {
        'username' : username,
    }


@register.inclusion_tag('card/keywords.html')
def keywords():
    keywords = KeyWords.objects.filter(is_active=True).order_by('show_order')
    return {'keywords':keywords}
    
@register.inclusion_tag('card/cardbox.html')
def cardbox():
    from gamecard.utils.strutils import get_ordered_act
    act_codes = Activity.objects.filter(card_type='act_code',status="active")
    begin_cards = Activity.objects.filter(card_type='begin_card',status="active")
    (a_hot,a_new,a_alpha) = get_ordered_act(begin_cards,start_alpha_index=12)
    (b_hot,b_new,b_alpha) = get_ordered_act(act_codes,start_alpha_index=2)
    return locals()

@register.inclusion_tag('card/news.html')
def news():
    anounces = Anounce.objects.all().order_by('-create_time')[0:MAX_ANOUNCE]
    notices = Notice.objects.all().order_by('-create_time')[0:MAX_NOTICE]
    pictures = Pictures.objects.filter(is_active=True).order_by('-create_time')
    return {
        'anounces':anounces,
        'notices':notices,
        'pictures':pictures,
    }
    
@register.inclusion_tag('card/popups/ad_pic.html')
def ad_pic():
    re_dict = {
        'pic_url':'',
        'link_url':'',
        'title':'',
    }
    ads = Advertise.objects.filter(is_active=True)   
    if bool(ads):
        count = len(ads)
        from random import randint
        index = randint(0,count-1)
        ad = ads[index]
        re_dict['pic_url'] = ad.img_url
        re_dict['title'] = ad.title
        re_dict['link_url'] = ad.link_url
    return re_dict
