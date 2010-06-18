#encoding:utf-8
from django.db import models
from datetime import datetime
import os
from tinymce import models as tinymce_models

class Games(models.Model):
    name = models.CharField("名称",max_length=50,unique=True)
    descri = models.TextField("描述",null=True,blank=True)
    game_type = models.CharField(max_length=10,verbose_name="游戏类型",choices=(('webpage','网页游戏'),("mmo",'客户端游戏')))
    create_time = models.DateTimeField("创建时间")
    class Meta:
        verbose_name = "游戏信息"
        verbose_name_plural = "游戏信息"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.name

CARD_FILE_FORMAT_TYPE = (('card_id','卡号'),('card_id&passwd','卡号和密码'),('card_id&count','推广码'))
class Item(models.Model):
    name = models.CharField("物品名称",max_length=50,unique=True)
    format = models.CharField("物品格式",max_length=25,choices=CARD_FILE_FORMAT_TYPE)
    pic = models.ImageField(upload_to='icons/',verbose_name="物品图片")
    is_chance = models.BooleanField("是否进入淘卡库",default=True)
    chance_time_delta = models.IntegerField("被领取后几小时进入淘卡库",default=2)
    max_apply_perday = models.IntegerField("每日最多领取次数",default=0)
    max_apply_perday_reminder = models.TextField("达到每日最多领取次数提示语",default="")
    info = models.TextField("物品信息",null=True,blank=True)
    descri = models.TextField("物品介绍",null=True,blank=True)
    class Meta:
        verbose_name = "物品信息"
        verbose_name_plural = "物品信息"
        #ordering = ['-chance_time']
    def __unicode__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField("活动名称",max_length=50,unique=True)
    name_start_alpha = models.CharField("名称首字母",max_length=1,help_text="必须大写！！！")
    item = models.ForeignKey(Item,verbose_name="对应物品")
    game = models.ForeignKey(Games,verbose_name="所属游戏")
    is_hot = models.BooleanField("是否热门游戏",default=False)
    card_count = models.IntegerField("发卡数量",default=0)
    award_percent = models.IntegerField("中奖机率",default=100,help_text="百分比(%)")
    card_type = models.CharField("发号类型",max_length=10,choices=(('act_code','激活码'),('begin_card','新手卡')))
    status = models.CharField("活动状态",max_length=10,default='wait',
        choices=(('active','已发布'),('wait','待发布'),('halt','停止')))
    descri = models.TextField("新手卡介绍",null=True,blank=True)#models.TextField("新手卡介绍",null=True,blank=True)
    info = models.TextField("详细内容",null=True,blank=True)
    reminder_award = models.TextField("中奖提示内容",null=True,blank=True)
    reminder_noaward = models.TextField("未中奖提示内容",null=True,blank=True)
    start_time = models.DateTimeField("活动开始时间") 
    class Meta:
        verbose_name = "活动信息"
        verbose_name_plural = "活动信息"
        ordering = ['-start_time']
    def card_left(self):
        from gamecard.utils.dbutils import get_mongodb_collect
        from gamecard.utils.strutils import get_collect_name
        collect = get_mongodb_collect(get_collect_name(self.item.id))
        return collect.find({"status":'normal'}).count()
    card_left.short_description = "卡号剩余量"
    #card_left.
    def __unicode__(self):
        return self.name  

class Notice(models.Model):
    title = models.CharField("公告标题",max_length=20,unique=True)
    activity = models.ForeignKey(Activity,verbose_name='所属活动')
    create_time = models.DateTimeField("创建时间")
    content = models.TextField("公告内容")
    class Meta:
        verbose_name = "活动公告"
        verbose_name_plural = "活动公告"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.title
        
class Anounce(models.Model):
    create_time = models.DateTimeField("创建时间")
    content = models.CharField("预告内容",max_length=20)
    class Meta:
        verbose_name = "发卡预告"
        verbose_name_plural = "发卡预告"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.content

class KeyWords(models.Model):
    title = models.CharField("内容",max_length=20)
    link_url = models.URLField(verbose_name="链接地址")
    is_active = models.BooleanField("是否激活",default=True)
    show_order = models.IntegerField("显示顺序号",help_text='从左至右依照序号大小排列')
    class Meta:
        verbose_name = "热点关键字"
        verbose_name_plural = "热点关键字"
    def __unicode__(self):
        return self.title
    
class Pictures(models.Model):
    title = models.CharField("内容",max_length=25)
    img_url = models.ImageField(upload_to='icons/',verbose_name="图片")
    link_url = models.URLField(verbose_name="链接地址")
    is_active = models.BooleanField("是否激活",default=True)
    create_time = models.DateTimeField("创建时间")
    class Meta:
        verbose_name = "广告发布"
        verbose_name_plural = "广告发布"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.title

class GameCompany(models.Model):
    company_name = models.CharField("公司名称",max_length=100)
    game_name = models.CharField("游戏名称",max_length=100)
    game_type = models.CharField(max_length=10,verbose_name="游戏类型",choices=(('webpage','网页游戏'),("mmo",'客户端游戏')))
    content = models.TextField("合作内容",max_length=500)
    contact_person = models.CharField("联系人姓名",max_length=100)
    person_position = models.CharField("联系人职位",max_length=100)
    contact = models.CharField("联系方式",max_length=100,help_text="（QQ、Msn、Email、电话、或其他联系方式）")
    create_time = models.DateTimeField("创建时间",null=True,blank=True,default=datetime.now())  
    class Meta:
        verbose_name = "发卡合作"
        verbose_name_plural = "发卡合作"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.company_name
        
class Suggest(models.Model):
    title = models.CharField("标题",max_length=100)
    content = models.TextField("内容",max_length=500)
    email = models.EmailField("电子邮箱",max_length=100)
    username = models.CharField("用户名",max_length=50)
    create_time = models.DateTimeField("创建时间",null=True,blank=True,default=datetime.now())
    class Meta:
        verbose_name = "用户反馈"
        verbose_name_plural = "用户反馈"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.title
    
    
class OnlineNews(models.Model):
    content = models.CharField("游戏名称",max_length=10)
    link_url = models.URLField(verbose_name="链接地址")
    status = models.CharField("状态",max_length=10)
    online_time = models.DateTimeField("上线时间")
    class Meta:
        verbose_name = "新游戏上线公告"
        verbose_name_plural = "新游戏上线公告"
    def __unicode__(self):
        return self.content
    
def get_cardfile_path(instance,filename):
    return "%s/%s-%s"%("card_files",instance.item.id,filename)
                   
class CardFileLoader(models.Model):
    item = models.ForeignKey(Item,verbose_name="对应物品")
    card_id_files = models.FileField(upload_to=get_cardfile_path,verbose_name="卡号文件")
    class Meta:
        verbose_name = "上传卡号"
        verbose_name_plural = "上传卡号"
    def __unicode__(self):
        return u"%s 卡号文件"%self.item.name
