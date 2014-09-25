from django import template
from core.models import is_user_logged

register = template.Library()

@register.filter(name='is_auth')
def is_auth(value):

    if not value.is_authenticated or value.is_anonymous():
        return False

    return is_user_logged(value)


