from django import template
from datetime import datetime


register = template.Library()


@register.filter(name='put_space')
def put_space(text):
    return text.replace('_', ' ')


@register.filter(name='format_date')
def format_date(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")


@register.filter(name='get_value')
def get_value(my_dict, key):
    return my_dict[key]


@register.filter(name='tc_amount_transfer')
def get_value(transfers):
    return f'{transfers * 750:,}'.replace(',', ' ')


@register.filter(name='tc_amount_name')
def get_value(name_change):
    return f'{name_change * 250:,}'.replace(',', ' ')


@register.filter(name='exp_with_space')
def get_value(exp):
    return f'{exp:,}'.replace(',', ' ')
