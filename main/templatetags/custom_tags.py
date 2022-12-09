from django import template


register = template.Library()


@register.filter(name='put_space')
def put_space(text):
    return text.replace('_', ' ')
