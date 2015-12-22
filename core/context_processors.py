from django.conf import settings
from core.models import is_user_registred


def important(request):
    return {
        'GOOGLE_ANALYTICS': settings.ON_VIPER and not settings.DEVEL,
        'graphics': request.user.profile.graphics if is_user_registred(request.user) else settings.DEFAULT_GRAPHICS,
        'DOMAIN': request.build_absolute_uri('/')[:-1],
    }