#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('card.views',
   ('get_card/(.+)/$','get_card'),
   ('get_chance/(.+)/$','get_chance'),
   ('login_bar/$','login_bar'),
   ('activitydetail/(.+).html$','activity_detail'),
   ('coperation/$','coperation'),
   ('suggest/$','suggest'),
   ('help/$','help'),
   ('cardbox/(.+)/(.+)/delete/$','delete_card'),
   ('cardbox/$','cardbox'),
   ('search/$','search'),
   ('itemdetail/(.+)/(.+)/$','item_detail'),
   ('get_check_code_image/$', 'get_check_code_image'),  
   ('','index'),
)

