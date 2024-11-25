# sistema/templatetags/custom_filters.py

from django import template
import base64

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

@register.filter
def base64_encode(image):
    try:
        with open(image.path, "rb") as img:
            return base64.b64encode(img.read()).decode('utf-8')
    except Exception as e:
        return ''