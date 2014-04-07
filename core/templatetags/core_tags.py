from django import template

register = template.Library()

@register.filter(name='is_auth')
def is_auth(value):

    if not value.is_authenticated:
        return False

    print "zde", value.social_auth.exists()


    return value.social_auth.exists()


