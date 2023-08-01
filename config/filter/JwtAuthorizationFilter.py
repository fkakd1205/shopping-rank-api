from flask import request, g
import requests

from domain.user.model.UserModel import UserModel
from config.key.prod.ProductionConfig import origin
from utils.cookie.CustomCookieUtils import CustomCookieUtils

class JwtAuthorizationFitler():

    def filter():
        jwt_token_cookie = request.cookies.get(CustomCookieUtils.COOKIE_NAME_ACCESS_TOKEN)
        if(jwt_token_cookie is None): return

        url = origin['auth-api'] + '/auth/v1/users/accessToken/getAccessKey'
        headers = {'Authorization': f"Bearer {jwt_token_cookie}"}
        response = requests.post(url=url, headers=headers)
        
        # 예외 세분화
        if(response.status_code != 200): return
        
        object = response.json()
        user_model = UserModel()
        user_model.id = object['data']
        
        g.user = user_model
