from django.http import HttpResponseRedirect
from core.models import is_user_logged


def non_lazy_required(view_function, redirect_to=None):
    return NonLazyRequired(view_function, redirect_to )

class NonLazyRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            redirect_to = "/"
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if not is_user_logged(request.user):
            return HttpResponseRedirect(self.redirect_to)
        return self.view_function(request, *args, **kwargs)