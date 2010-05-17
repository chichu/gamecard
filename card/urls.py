#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('card.views',
   ('get_card/(.+)/$','get_card'),
   ('get_chance/(.+)/$','get_chance'),
   ('activitydetail/(.+).html$','activity_detail'),
   ('coperation/','coperation'),
   ('itemdetail/(.+).html$','item_detail'),
   ('get_check_code_image/$', 'get_check_code_image'),  
   ('','index'),
)
