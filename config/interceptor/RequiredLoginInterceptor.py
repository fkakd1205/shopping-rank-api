from flask import g

from exception.types.CustomException import CustomInvalidUserException

def required_login(func):
    def wrapper(self, *args, **kwargs):
        try:
            if(g.get('user') is None): raise
        except (KeyError, Exception):
            raise CustomInvalidUserException("로그인이 필요한 서비스입니다.")
        
        return func(self, *args, **kwargs)
        
    return wrapper
