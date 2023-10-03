from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def tostring(value):
    return str(value)

@register.filter
def tostrip(value):
    return value.split(' ')[0]