import os
import jwt
import base64
from datetime import datetime
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

JWT_API_ISSUER = os.environ.get('JWT_API_ISSUER')

class CustomJwtUtils():
    CSRF_TOKEN_JWT_EXPIRATION = 15 * 60 * 1000

    def generate_jwt_token(self, subject, expiration_time, secret):
        encoded = jwt.encode(
            payload=self.create_token_payload(subject, expiration_time),
            key=self.generate_signinig_key(secret),
            algorithm='HS256',
            headers=self.create_token_header()
        )
        
        return encoded
    
    def parse_jwt(self, secret, token):
        claims = jwt.decode(
            jwt=token,
            key=self.generate_signinig_key(secret),
            algorithms='HS256'
        )
        return claims
    
    def generate_signinig_key(self, secret):
        key_bytes = secret.encode('utf8')
        key_bytes64 = base64.b64encode(key_bytes)
        return key_bytes64

    def create_token_issued_at(self):
        return int(round(datetime.utcnow().timestamp()))
    
    def create_token_payload(self, subject, expiration_time):
        return {
            "iss": JWT_API_ISSUER,
            "sub": subject,
            "iat": self.create_token_issued_at(),
            "exp": self.create_token_expiration(expiration_time)
        }
    
    def create_token_header(self):
        return {
            "typ": "JWT",
            "alg": "HS256",
            "regDate": self.create_token_issued_at()
        }
    
    def create_token_expiration(self, expiration_time):
        expiration = int(round(datetime.utcnow().timestamp())) + expiration_time
        return expiration