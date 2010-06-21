# encoding: utf-8
class AuthMiddleware(object):
    def process_request(self, request):
        if not request.session.has_key('username'):
            request.session['username'] = get_username_from_cookie(request)
        return None