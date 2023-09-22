from flask import request
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from werkzeug.http import dump_cookie

from utils import * 
from exception.types.CustomException import *

class CsrfAuthenticationFilter():
    CSRF_TOKEN_SECRET = CsrfTokenUtils().get_csrf_token_secret()
    CSRF_WHITELIST_URL = WhitelistUrlUtils().get_csrf_whitelist_url()

    def filter(self):
        whitelist = self.CSRF_WHITELIST_URL
        request_method = request.method
        # request_url = request.url
        request_path = request.path
        request_header = request.headers
        request_cookies = request.cookies

        if(request_method in ["GET", "OPTIONS"]):
            return
        else:
            try:
                csrf_whitelist_urls = whitelist.get(request_method, [])
                
                # whitelist origin 통과
                if(request_path in csrf_whitelist_urls):
                    return

                csrf_jwt_token = request_cookies.get(CustomCookieUtils.COOKIE_NAME_API_CSRF_TOKEN)
                x_csrf_token = request_header['X-XSRF-TOKEN']

                secret = x_csrf_token + self.CSRF_TOKEN_SECRET
                CustomJwtUtils().parse_jwt(secret, csrf_jwt_token)
            except ExpiredSignatureError:
                raise CustomCsrfJwtExpiredException("Csrf jwt expired.")
            except InvalidSignatureError:
                raise CustomCsrfJwtAccessDeniedException("Csrf jwt signature validation fails.")
            except DecodeError:
                raise CustomCsrfJwtDecodeException("Csrf jwt can't decode")
    
    def clear_all_csrf_tokens(self, response):
        csrf_jwt = dump_cookie(
                key=CustomCookieUtils.COOKIE_NAME_API_CSRF_TOKEN,
                value="",
                httponly=True,
                domain=CustomCookieUtils.COOKIE_DOMAIN,
                secure=CustomCookieUtils.SECURE,
                samesite="Strict",
                path="/",
                max_age=0
            )
        
        csrf_token = dump_cookie(
                key=CustomCookieUtils.COOKIE_NAME_X_API_CSRF_TOKEN,
                value="",
                domain=CustomCookieUtils.COOKIE_DOMAIN,
                secure=CustomCookieUtils.SECURE,
                samesite="Strict",
                path="/",
                max_age=0
            )
        
        csrf_expired_at = dump_cookie(
                key=CustomCookieUtils.COOKIE_NAME_API_CSRF_EXPIRED_AT,
                value="",
                secure=CustomCookieUtils.SECURE,
                domain=CustomCookieUtils.COOKIE_DOMAIN,
                samesite="Strict",
                path="/",
                max_age=0
            )

        response.headers.add("Set-Cookie", csrf_jwt)
        response.headers.add("Set-Cookie", csrf_token)
        response.headers.add("Set-Cookie", csrf_expired_at)
