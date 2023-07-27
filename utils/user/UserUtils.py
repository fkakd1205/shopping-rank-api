from flask import request

from exception.types.CustomException import CustomInvalidUserException

class UserUtils():
    def get_user_id_else_throw(self):
        user_model = request.context['user']
        if(user_model is None): raise CustomInvalidUserException

        return user_model.id

        