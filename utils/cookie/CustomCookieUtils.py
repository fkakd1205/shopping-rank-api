from config.server.ServerConfig import config

class CustomCookieUtils():
    COOKIE_DOMAIN = config['cookie']['domain']
    SECURE = config['cookie']['secure']

    CSRF_TOKEN_COOKIE_EXPIRATION = 15 * 60
    API_CSRF_TOKEN_EXPIRED_AT_COOKIE_EXPIRATION = 5 * 60

    PHONE_VALIDATION_COOKIE_EXPIRATION = 30 * 60
    EMAIL_VALIDATION_COOKIE_EXPIRATION = 30 * 60
    ACCESS_TOKEN_COOKIE_EXPIRATION = 5 * 24 * 60 * 60

    COOKIE_NAME_ACCESS_TOKEN = "cp_ac_token"
    COOKIE_NAME_API_CSRF_TOKEN = "api_csrf_token"
    COOKIE_NAME_X_API_CSRF_TOKEN = "x_api_csrf_token"
    COOKIE_NAME_API_CSRF_EXPIRED_AT = "api_csrf_expired_at"