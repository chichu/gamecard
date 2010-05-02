#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('card.views',
   ('get_card/(.+)/','get_card'),
   ('get_chance/(.+)/','get_chance'),
   ('activitydetail/(.+)/$','activity_detail'),
   ('','index'),
)
