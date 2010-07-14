#encoding:utf-8

from models import *
from django.contrib import admin
from gamecard.utils.strutils import insert_card_ids,check_cardfile_format

class GamesAdmin(admin.ModelAdmin):
    list_display = ('name','game_type','create_time')
    search_fields = ('name',)
    radio_fields = {"game_type": admin.HORIZONTAL}
    list_filter = ('game_type',)
    readonly_fields = ('create_time',)
admin.site.register(Games,GamesAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','format','is_chance','chance_time_delta','max_apply_perday')
    search_fields = ('name',)
    radio_fields = {"format":admin.HORIZONTAL}
    list_filter = ('format','is_chance')
admin.site.register(Item,ItemAdmin)

class SuggestAdmin(admin.ModelAdmin):
    list_display = ('title','content','email','username','create_time')
    search_fields = ('title','content','email','username')
admin.site.register(Suggest,SuggestAdmin)

class GameCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name','game_name','game_type','content','contact_person','person_position','contact','create_time')
    search_fields = ('company_name','game_name','contact_person')
    radio_fields = {"game_type":admin.HORIZONTAL}
admin.site.register(GameCompany,GameCompanyAdmin)

class ActAdmin(admin.ModelAdmin):
    list_display = ('name','item','game','card_count','card_left','card_out_yesterday','get_yesterday','chance_yesterday','card_type','start_time','status')
    search_fields = ('name',)
    list_filter = ('status','card_type')
    list_per_page = 20
    radio_fields = {"status": admin.HORIZONTAL,"card_type":admin.HORIZONTAL}
admin.site.register(Activity,ActAdmin)

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title','content','activity','create_time')
    search_fields = ('title',)
admin.site.register(Notice,NoticeAdmin)

class KeyWordsAdmin(admin.ModelAdmin):
    list_display = ('title','link_url','show_order','is_active')
    search_fields = ('title',)
admin.site.register(KeyWords,KeyWordsAdmin)

class AnounceAdmin(admin.ModelAdmin):
    list_display = ('content','create_time')
    search_fields = ('content',)
admin.site.register(Anounce,AnounceAdmin)

class OnlineNewsAdmin(admin.ModelAdmin):
    list_display = ('content','online_time','status','link_url')
    search_fields = ('content',)
admin.site.register(OnlineNews,OnlineNewsAdmin)

class PictureAdmin(admin.ModelAdmin):
    list_display = ('title','link_url','create_time')
    search_fields = ('title',)
admin.site.register(Pictures,PictureAdmin)

class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('title','link_url','create_time')
    search_fields = ('title',)
admin.site.register(Advertise,AdvertiseAdmin)

class FileLoaderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change): 
        format = obj.item.format
        all_lines = obj.card_id_files.readlines()
        first_line = all_lines[0] 
        total_lines = len(all_lines)
        if total_lines == 0 or not check_cardfile_format(first_line,format):
            request.user.message_set.create(message=u"文件不符合格式！")
            return None
        count = insert_card_ids(all_lines,obj.item)
        Activity.objects.filter(item=obj.item).update(card_count=count)
admin.site.register(CardFileLoader,FileLoaderAdmin)
