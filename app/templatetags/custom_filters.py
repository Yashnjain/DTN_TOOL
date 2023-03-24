from django import template


register = template.Library()



@register.filter(name='add_floats')
def add_floats(value, arg):
    """
    Adds two float values.
    """
    try:
        return round(float(value) + float(arg),4)
    except (ValueError, TypeError):
        return ''
