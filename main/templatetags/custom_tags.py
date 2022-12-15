from django import template


register = template.Library()


@register.filter(name='put_space')
def put_space(text):
    return text.replace('_', ' ')


@register.filter(name='format_date')
def format_date(date):
    return date[:date.index('T')]
