from datetime import datetime, timedelta
from werkzeug.http import dump_cookie
import uuid

from utils import *

class CsrfTokenService():

    def get_csrf_token(self, response):
        csrf_token_id = str(uuid.uuid4())
        csrf_jwt_token = CsrfTokenUtils().generate_csrf_jwt_token(csrf_token_id)

        csrf_jwt = dump_cookie(
                key=CustomCookieUtils.COOKIE_NAME_API_CSRF_TOKEN,
                value=csrf_jwt_token,
                httponly=True,
                domain=CustomCookieUtils.COOKIE_DOMAIN,
                secure=CustomCookieUtils.SECURE,
                samesite="Strict",
                path="/",
                max_age=CustomCookieUtils.CSRF_TOKEN_COOKIE_EXPIRATION
            )
        
        csrf_token = dump_cookie(
                key=CustomCookieUtils.COOKIE_NAME_X_API_CSRF_TOKEN,
                value=csrf_token_id,
                domain=CustomCookieUtils.COOKIE_DOMAIN,
                secure=CustomCookieUtils.SECURE,
                samesite="Strict",
                path="/",
                max_age=CustomCookieUtils.CSRF_TOKEN_COOKIE_EXPIRATION
            )
        
        csrf_expired_at_time = CustomUTCDateTime.convert_timezone_format(datetime.utcnow() + timedelta(seconds=CustomCookieUtils.API_CSRF_TOKEN_EXPIRED_AT_COOKIE_EXPIRATION))
        csrf_expired_at = dump_cookie(
                key=CustomCookieUtils.COOKIE_NAME_API_CSRF_EXPIRED_AT,
                value=csrf_expired_at_time,
                secure=CustomCookieUtils.SECURE,
                domain=CustomCookieUtils.COOKIE_DOMAIN,
                samesite="Strict",
                path="/",
                max_age=CustomCookieUtils.API_CSRF_TOKEN_EXPIRED_AT_COOKIE_EXPIRATION
            )
        
        response.headers.add("Set-Cookie", csrf_jwt)
        response.headers.add("Set-Cookie", csrf_token)
        response.headers.add("Set-Cookie", csrf_expired_at)
