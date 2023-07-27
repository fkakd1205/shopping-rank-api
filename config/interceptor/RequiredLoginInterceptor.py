from flask import request

from exception.types.CustomException import CustomInvalidUserException

def required_login(func):
    def wrapper(self, *args):
        try:
            if(request.context['user'] is None): raise
        except (KeyError, Exception):
            raise CustomInvalidUserException("로그인이 필요한 서비스입니다.")
        
        func(self, *args)
        
    return wrapper
