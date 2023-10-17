from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record.service.NRankRecordService import NRankRecordService
from domain.nrank_record_info.service.NRankRecordInfoService import NRankRecordInfoService

from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum
from decorators import *

NRankRecordApi = Namespace('NRankRecordApi')

@NRankRecordApi.route('', methods=['POST'])
class NRankRecord(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_CREATE
    })
    def post(self):
        message = MessageDto()
        
        nRankRecordService = NRankRecordService()
        nRankRecordService.create_one()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/<id>', methods=['DELETE'])
class NRankRecordIncludeId(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_DELETE
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
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE,
        WorkspaceAccessTypeEnum.STORE_RANK_CREATE
    })
    @transactional()
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
        nRankRecordInfoService.check_allowed_search_count()
        
        nRankRecordService.change_status(id, NRankRecordStatusEnum.PENDING)
        nRankRecordInfoService.create_one(id)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/target:status/action:fail', methods=['PATCH'])
class NRankRecordChangeStatus(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE,
        WorkspaceAccessTypeEnum.STORE_RANK_DELETE
    })
    @transactional()
    def patch(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordInfoService = NRankRecordInfoService()
        
        nRankRecordService.change_list_status(NRankRecordStatusEnum.FAIL)
        nRankRecordInfoService.change_list_status_to_fail()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordApi.route('/workspace-usage-info', methods=['GET'])
class NRankRecordWorkspaceUsageInfo(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
    })
    def get(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        message.set_data(nRankRecordService.get_workspace_usage_info())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/<id>/target:category', methods=['PATCH'])
class NRankRecordChangeCategoryId(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE
    })
    def patch(self, id):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        
        nRankRecordService.change_category_id(id)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/slice', methods=['GET'])
class NRankRecordSlice(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        # message.set_data(nRankRecordService.search_list_and_related_latest_infos())
        message.set_data(nRankRecordService.search_list_and_related_info())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordApi.route('/count', methods=['GET'])
class NRankRecordCount(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        message.set_data(nRankRecordService.search_list_count())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code