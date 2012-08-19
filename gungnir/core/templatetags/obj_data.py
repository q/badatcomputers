from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def classname(obj, arg=None):
    classname = obj.__class__.__name__
    if arg:
        if arg.lower() == classname:
            return True
        else:
            return False
    else:
        return classname