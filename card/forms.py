# encoding: utf-8
from django import forms
from gamecard.utils import recaptcha

class CheckCodeForm(recaptcha.RecaptchaForm):
    captcha = recaptcha.RecaptchaField()

