#encoding:utf-8
from django.conf.urls.defaults import *
from models import 

urlpatterns = patterns('card.views',
   ('get_card/(.+)/$','get_card'),
   ('get_chance/(.+)/$','get_chance'),
   ('activitydetail/(.+).html$','activity_detail'),
   ('coperation/$','coperation'),
   ('suggest/$','suggest'),
   ('anounces/$','django.views.generic.list_detail.object_list',{"queryset":Anounce.objects.all().order_by('-create_time'),"paginate_by":30}),
   ('notices/$','django.views.generic.list_detail.object_list',{"queryset":Notice.objects.all().order_by('-create_time'),"paginate_by":30}),
   ('cardbox/(.+)/(.+)/delete/$','delete_card'),
   ('cardbox/$','cardbox'),
   ('search/$','search'),
   ('itemdetail/(.+)/(.+)/$','item_detail'),
   ('get_check_code_image/$', 'get_check_code_image'),  
   ('','index'),
)
