from flask_restx import Namespace, Resource
from http import HTTPStatus
import time
from domain.message.dto.MessageDto import MessageDto
from utils.db.v2.DBUtils import db_session

TestApi = Namespace('TestApi')

@TestApi.route('', methods=['GET'])
class Test(Resource):
    def get(self):
        message = MessageDto()
        
        print(db_session())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")
        time.sleep(5)

        return message.__dict__, message.status_code
