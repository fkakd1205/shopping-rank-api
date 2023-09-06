import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv
from utils.jwt.CustomJWTUtils import CustomJwtUtils

custom_load_dotenv()

CSRF_TOKEN_SECRET = os.environ.get('CSRF_JWT_SECRET')

class CsrfTokenUtils():
    
    def generate_csrf_jwt_token(self, x_csrf_token):
        secret = x_csrf_token + CSRF_TOKEN_SECRET
        
        return CustomJwtUtils().generate_jwt_token(
            "CSRF_JWT",
            CustomJwtUtils.CSRF_TOKEN_JWT_EXPIRATION,
            secret
        )

    def get_csrf_token_secret(self):
        return CSRF_TOKEN_SECRET
