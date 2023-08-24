from flask_restx import Namespace, Resource
from http import HTTPStatus
import time
import threading

from domain.message.dto.MessageDto import MessageDto
from utils import db_session
from domain.test.TestService import TestService
# from domain.test.TestService import test
from domain.workspace.service.WorkspaceAuthService import WorkspaceAuthService

# from decorators.required_login import required_login

from decorators import *
from exception.types.CustomException import *
from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum

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

    # @required_login
    # @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
    #     WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    # })

    def get(self):
        message = MessageDto()
        testService = TestService()
        
        # TODO :: args에 아무것도 없을 경우
        threading.Thread(target=testService.test, args=(), daemon=True).start()
        # testService.test2()

        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    