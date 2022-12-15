from django import template
from datetime import datetime


register = template.Library()


@register.filter(name='put_space')
def put_space(text):
    return text.replace('_', ' ')


@register.filter(name='format_date')
def format_date(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
