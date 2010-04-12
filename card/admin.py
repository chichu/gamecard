#encoding:utf-8

from models import *
from django.contrib import admin
from gamecard.utils.dbutils import insert_card_ids

class GamesAdmin(admin.ModelAdmin):
    list_display = ('name','game_type','create_time')
    search_fields = list_display
    radio_fields = {"game_type": admin.HORIZONTAL}
    list_filter = ('game_type',)
    readonly_fields = ('create_time',)
admin.site.register(Games,GamesAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','format','is_chance','chance_time','max_apply_perday')
    search_fields = list_display
    radio_fields = {"format":admin.HORIZONTAL}
    list_filter = ('format','is_chance')
admin.site.register(Item,ItemAdmin)

class ActAdmin(admin.ModelAdmin):
    list_display = ('name','item','game','card_count','start_time','status')
    search_fields = list_display
    list_filter = ('status',)
    radio_fields = {"status": admin.HORIZONTAL}
admin.site.register(Activity,ActAdmin)
   
class FileLoaderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change): 
        format = obj.item.format
        first_line = obj.card_id_files.readline()
        if len(all_lines) == 0 or check_cardfile_format(first_line,format):
            request.user.message_set.create(message=u"文件不符合格式！")
            return None
        all_lines = obj.card_id_files.readlines()
        if not insert_card_ids(all_lines,obj.item):
            request.user.message_set.create(message=u"部分卡号不符合格式或者重复:%s"%",".join(error_id_set))    
admin.site.register(CardFileLoader,FileLoaderAdmin)



