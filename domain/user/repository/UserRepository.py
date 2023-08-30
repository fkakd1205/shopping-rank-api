from utils.db.v2.DBUtils import db_session
from sqlalchemy import select

from domain.user.model.UserModel import UserModel

class UserRepository():

    def search_one_by_username(username):
        query = select(UserModel).where(UserModel.username == username)
        return db_session.execute(query).scalar()