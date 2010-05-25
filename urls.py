#encoding:utf-8

from django.conf.urls.defaults import *
from settings import MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from gamecard.card.models import Anounce,Notice

urlpatterns = patterns('',
    (r'^card/anounces/$','django.views.generic.list_detail.object_list',{"queryset":Anounce.objects.all().order_by('-create_time'),"paginate_by":15}),
    (r'^card/notices/$','django.views.generic.list_detail.object_list',{"queryset":Notice.objects.all().order_by('-create_time'),"paginate_by":15}),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r"^card/",include('gamecard.card.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^$', 'gamecard.card.views.index'),
)

