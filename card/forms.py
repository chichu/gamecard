# encoding: utf-8
from django import forms
from models import GameCompany,Suggest

class CoperationForm(forms.ModelForm):
    class Meta:
        model = GameCompany
        exclude = ('create_time',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'game_type':forms.RadioSelect()
        }
        
class SuggestForm(forms.ModelForm):
    class Meta:
        model = Suggest
        exclude = ('create_time','username')
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
        }

