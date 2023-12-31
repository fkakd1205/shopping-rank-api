from flask import g

from exception.types.CustomException import CustomInvalidUserException

class UserUtils():
    def get_user_id_else_throw(self):
        user_model = g.get('user')
        if(user_model is None): raise CustomInvalidUserException('로그인이 필요한 서비스 입니다.')

        return user_model.id
    