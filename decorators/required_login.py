from flask import g, request
import requests

from domain.user.model.UserModel import UserModel
from config.key.prod.ProductionConfig import origin
from utils import CustomCookieUtils
from exception.types.CustomException import CustomInvalidUserException

def required_login(func):
    def wrapper(self, *args, **kwargs):
        jwt_token_cookie = request.cookies.get(CustomCookieUtils.COOKIE_NAME_ACCESS_TOKEN)
        if(jwt_token_cookie is None): raise CustomInvalidUserException('로그인이 필요한 서비스 입니다.')

        url = origin['auth-api'] + '/auth/v1/users/accessToken/getAccessKey'
        headers = {'Authorization': f"Bearer {jwt_token_cookie}"}
        response = requests.post(url=url, headers=headers)
        
        # 예외 세분화
        if(response.status_code != 200): raise CustomInvalidUserException('로그인이 필요한 서비스 입니다.')
        
        object = response.json()
        user_model = UserModel()
        user_model.id = object['data']
        
        g.user = user_model

        return func(self, *args, **kwargs)
    return wrapper
