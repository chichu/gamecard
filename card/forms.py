# encoding: utf-8
from django import forms
from models import GameCompany,Suggest
from gamecard.utils import recaptcha

class CheckCodeForm(recaptcha.RecaptchaForm):
    captcha = recaptcha.RecaptchaField()
    
class CoperationForm(forms.ModelForm):
    class Meta:
        model = GameCompany
        exclude = ('create_time',)
        
class SuggestForm(forms.ModelForm):
    class Meta:
        model = Suggest
        exclude = ('create_time','username')

