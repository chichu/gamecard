# encoding: utf-8
from django import template

register = template.Library()

@register.inclusion_tag('card/headnav.html')
def headnav(nav_index):
    return {
        'nav_index' : nav_index,
    }


