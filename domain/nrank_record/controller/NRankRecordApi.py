from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record.service.NRankRecordService import NRankRecordService
from domain.workspace.service.WorkspaceService import WorkspaceService
from domain.nrank_record_info.service.NRankRecordInfoService import NRankRecordInfoService

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
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
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
        """change nrank record status to pending
        
        1. 랭킹 조회 횟수 검사
        2. change status
        3. create info and return id
        id -- record_id
        """
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordInfoService = NRankRecordInfoService()
        workspaceService = WorkspaceService()
        workspaceService.check_nrank_search_allowed_count()
        
        nRankRecordService.change_status(id, NRankRecordStatusEnum.PENDING)
        message.set_data(nRankRecordInfoService.create_one_and_get_id(id))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/target:status/action:fail', methods=['PATCH'])
class NRankRecordChangeStatus(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def patch(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordInfoService = NRankRecordInfoService()
        
        nRankRecordService.change_list_status(NRankRecordStatusEnum.FAIL)
        nRankRecordInfoService.change_list_status_to_fail()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
