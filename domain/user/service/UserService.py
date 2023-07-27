from domain.user.repository.UserRepository import UserRepository
from exception.types.CustomException import CustomInvalidUserException

class UserService():
    
    def search_one_by_username(self, username):
        user_repository = UserRepository()
        user_model = user_repository.search_one_by_username(username)
        if(user_model is None) : raise CustomInvalidUserException("로그인 회원이 아니거나, 잘못된 접근방식임.")
        return user_model
