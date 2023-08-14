from flask_restx import Namespace, Resource
from http import HTTPStatus
import time
import threading
from domain.message.dto.MessageDto import MessageDto
from utils.db.v2.DBUtils import db_session
from domain.test.TestService import TestService

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

    def get(self):
        message = MessageDto()
        testService = TestService()

        

        t1 = threading.Thread(target=testService.test, daemon=True)
        t2 = threading.Thread(target=testService.test, daemon=True)
    
        t1.start()
        t2.start()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
def test():
    print("hii22")
    time.sleep(5)
    