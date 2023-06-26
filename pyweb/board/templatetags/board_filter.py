from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg  #원래값 - 매개값 해주고 return -> |sub:arg 식으로 표기