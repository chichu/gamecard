# encoding: utf-8
from gamecard.utils.strutils import get_userinfo_from_cookie
from gamecard.log import log_error

class AuthMiddleware(object):
    def process_request(self, request):
        try:
            #if not request.session.has_key('username'):
            user_info = get_userinfo_from_cookie(request)
            request.session['username'] = user_info['username']
            request.session['uid'] = user_info['uid']
        except Exception,e:
            log_error("error in Authmiddleware:%s request sesion:%s"%(e,request.session['username']))
            return None
        return None
