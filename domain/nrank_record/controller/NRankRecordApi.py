from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record.service.NRankRecordService import NRankRecordService
from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

from config.interceptor.RequiredLoginInterceptor import required_login
from config.interceptor.RequiredWorkspaceAuthInterceptor import required_workspace_auth

NRankRecordApi = Namespace('NRankRecordApi')

@NRankRecordApi.route('', methods=['GET', 'POST'])
class NRankRecord(Resource):

    @required_login
    @required_workspace_auth(check_access_type_flag = True, required_access_types = {
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
    @required_workspace_auth(check_access_type_flag = True, required_access_types = {
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
    
@NRankRecordApi.route('/search', methods=['POST'])
class NRankRecordIncludesIds(Resource):
    
    @required_login
    @required_workspace_auth(check_access_type_flag = True, required_access_types = {
        # TODO :: 워크스페이스 타입 변경
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def post(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        message.set_data(nRankRecordService.search_list_by_ids())
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
    def patch(self, id):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordService.change_status(id, NRankRecordStatusEnum.PENDING)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordApi.route('/<id>/target:status/action:fail', methods=['PATCH'])
class NRankRecordChangeStatus(Resource):
    
    @required_login
    def patch(self, id):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordService.change_status(id, NRankRecordStatusEnum.FAIL)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
