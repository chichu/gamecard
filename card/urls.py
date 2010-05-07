#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('card.views',
   ('get_card/(.+)/$','get_card'),
   ('get_chance/(.+)/$','get_chance'),
   ('activitydetail/(.+).html$','activity_detail'),
   ('act_codes/(.+)/$','act_codes'),
   ('begin_cards/(.+)/$','begin_cards'),
   ('pictures/$','pictures'),
   ('anounces/$','anounces'),
   ('notices/$','notices'),
   ('keywords/$','keywords'),
   ('get_check_code_image/$', 'get_check_code_image'),  
   ('','index'),
)
