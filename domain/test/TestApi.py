from flask_restx import Namespace, Resource
from http import HTTPStatus
import time
import threading

from domain.message.dto.MessageDto import MessageDto
from utils.db.v2.DBUtils import db_session
from domain.test.TestService import TestService
# from decorators.required_login import required_login
# from decorators.using_db import using_db

from decorators import *
from exception.types.CustomException import *

TestApi = Namespace('TestApi')

@TestApi.route('', methods=['GET'])
class Test(Resource):
    # def get(self):
    #     message = MessageDto()
        
    #     print(db_session())
    #     message.set_status(HTTPStatus.OK)
    #     message.set_message("success")
    #     time.sleep(5)

    #     return message.__dict__, message.status_code

    @using_db()
    def get(self):
        message = MessageDto()
        testService = TestService()

        # raise CustomInvalidUserException('invalid')
        message.set_data(testService.test())
        
        # t1 = threading.Thread(target=testService.test, daemon=True)
        # t2 = threading.Thread(target=testService.test, daemon=True)
    
        # t1.start()
        # t2.start()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    