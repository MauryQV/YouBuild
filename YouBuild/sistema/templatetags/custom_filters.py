# sistema/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplica dos números.
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
