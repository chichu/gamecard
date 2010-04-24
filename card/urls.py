#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('card.views',
   #('r^get_card','user.get_card'),
   ('gamedetail/','detail'),
   ('','index'),
)
