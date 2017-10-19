from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [compile(settings.LOGIN_URL.lstrip('/')), compile('/api/set-ac'.lstrip('/'))]

    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def __call__(self, request):
        response = self.get_response(request)
        assert hasattr(request, 'user')

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/') 
            if not any(m.match(path) for m in self.exempt_urls):
                return HttpResponseRedirect(settings.LOGIN_URL)

        return response
