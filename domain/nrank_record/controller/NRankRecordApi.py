from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record.service.NRankRecordService import NRankRecordService
from domain.workspace.service.WorkspaceAuthService import WorkspaceAuthService

from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

from decorators import *

NRankRecordApi = Namespace('NRankRecordApi')

@NRankRecordApi.route('', methods=['GET', 'POST'])
class NRankRecord(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def post(self):
        message = MessageDto()
        
        nRankRecordService = NRankRecordService()
        nRankRecordService.create_one()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        # TODO :: 워크스페이스 타입 변경
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def get(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        message.set_data(nRankRecordService.search_list())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/<id>', methods=['DELETE'])
class NRankRecordIncludeId(Resource):
    
    @required_login
    def delete(self, id):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordService.delete_one(id)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordApi.route('/<id>/target:status/action:pending', methods=['PATCH'])
class NRankRecordChangeStatus(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def patch(self, id):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        workspaceAuthService = WorkspaceAuthService()
        workspaceAuthService.check_nrank_search_allowed_count()

        nRankRecordService.change_status(id, NRankRecordStatusEnum.PENDING)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/target:status/action:fail', methods=['PATCH'])
class NRankRecordChangeStatus(Resource):
    
    @required_login
    def patch(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordService.change_list_status(NRankRecordStatusEnum.FAIL)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code