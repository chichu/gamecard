#encoding:utf-8
from django.db import models
from datetime import datetime
import os
from tinymce import models as tinymce_models

class Games(models.Model):
    name = models.CharField("名称",max_length=50,unique=True)
    descri = tinymce_models.HTMLField("描述",null=True,blank=True)
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
    max_apply_perday_reminder = tinymce_models.HTMLField("达到每日最多领取次数提示语",default="")
    info = tinymce_models.HTMLField("物品信息",null=True,blank=True)
    descri = tinymce_models.HTMLField("物品介绍",null=True,blank=True)
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
    descri = tinymce_models.HTMLField("新手卡介绍",null=True,blank=True)
    info = tinymce_models.HTMLField("详细内容",null=True,blank=True)
    reminder_award = tinymce_models.HTMLField("中奖提示内容",null=True,blank=True)
    reminder_noaward = tinymce_models.HTMLField("未中奖提示内容",null=True,blank=True)
    start_time = models.DateTimeField("活动开始时间") 
    class Meta:
        verbose_name = "活动信息"
        verbose_name_plural = "活动信息"
        ordering = ['-start_time']
    def __unicode__(self):
        return self.name  

class Notice(models.Model):
    title = models.CharField("公告标题",max_length=20,unique=True)
    activity = models.ForeignKey(Activity,verbose_name='所属活动')
    create_time = models.DateTimeField("创建时间")
    content = tinymce_models.HTMLField("公告内容")
    class Meta:
        verbose_name = "活动公告"
        verbose_name_plural = "活动公告"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.title
        
class Anounce(models.Model):
    create_time = models.DateTimeField("创建时间")
    content = models.CharField("预告内�",max_length=50)
    class Meta:
        verbose_name = "发卡预告"
        verbose_name_plural = "发卡预告"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.content

class Pictures(models.Model):
    title = models.CharField("内容",max_length=25,choices=CARD_FILE_FORMAT_TYPE)
    img_url = models.ImageField(upload_to='icons/',verbose_name="图片")
    link_url = models.CharField(max_length=100,verbose_name="链接地址")
    is_active = models.BooleanField("是否激活",default=True)
    create_time = models.DateTimeField("创建时间")
    class Meta:
        verbose_name = "广告发布"
        verbose_name_plural = "广告发布"
        ordering = ['-create_time']
    def __unicode__(self):
        return self.title
    
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
