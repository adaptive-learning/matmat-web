from django.conf import settings


def important(request):
    return {'GOOGLE_ANALYTICS': settings.ON_VIPER and not settings.DEVEL}