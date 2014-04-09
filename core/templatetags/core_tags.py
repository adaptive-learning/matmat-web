from django import template

register = template.Library()

@register.filter(name='is_auth')
def is_auth(value):

    if not value.is_authenticated or value.is_anonymous():
        return False

    return value.social_auth.exists()


