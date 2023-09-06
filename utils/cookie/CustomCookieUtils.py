import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

class CustomCookieUtils():
    COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN')
    SECURE = os.environ.get('COOKIE_SECURE')
    CSRF_TOKEN_COOKIE_EXPIRATION = 15 * 60; 
    API_CSRF_TOKEN_EXPIRED_AT_COOKIE_EXPIRATION = 5 * 60

    COOKIE_NAME_ACCESS_TOKEN = "cp_ac_token"
    COOKIE_NAME_API_CSRF_TOKEN = "nrank_api_csrf_token"
    COOKIE_NAME_X_API_CSRF_TOKEN = "x_nrank_api_csrf_token"
    COOKIE_NAME_API_CSRF_EXPIRED_AT = "nrank_api_csrf_expired_at"