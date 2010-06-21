# encoding: utf-8
from gamecard.utils.strutils import get_username_from_cookie
from gamecard.log import log_error

class AuthMiddleware(object):
    def process_request(self, request):
        try:
            #if not request.session.has_key('username'):
            request.session['username'] = get_username_from_cookie(request)
        except Exception,e:
            log_error("error in Authmiddleware:%s request sesion:%s"%(e,request.session['username']))
            return None
        return None
