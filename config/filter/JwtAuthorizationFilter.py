import jwt
from flask import request, g
import base64

from domain.user.model.UserModel import UserModel
from config.key.jwt.JwtKeyConfig import jwt_secret

class JwtAuthorizationFitler():
    def filter():
        # TODO :: excludeUrls 추가

        jwt_token_cookie = request.cookies.get('cp_ac_token')
        # jwt_token_cookie가 None일 때, csrf검사
        # if(jwt_token_cookie is None): return
        
        # secret_key = jwt_secret['access_token'].encode('utf-8')
        # key_bytes = base64.b64encode(secret_key)

        # TODO :: decode 설정
        # claims = jwt.decode(jwt_token_cookie, key_bytes, algorithms=['HS256'])

        # id = claims.id
        # username = claims.username
        id = "212935ba-a222-40a6-8827-dcafedd3cd6c"
        username = "user111"
        
        user_model = UserModel()
        user_model.id = id
        user_model.username = username

        g.user = user_model