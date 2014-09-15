from django.contrib.auth import logout
from django.shortcuts import redirect
from social_auth.exceptions import AuthAlreadyAssociated


class AuthAlreadyAssociatedMiddleware(object):
    '''
    Solve problem between lazysingup and social_auth
    which appear after logout
    '''

    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            url = request.path # should be something like '/complete/google/'
            url = url.replace("complete", "login")
            logout(request)
            return redirect(url)
