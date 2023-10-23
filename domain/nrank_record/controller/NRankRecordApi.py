from flask_restx import Namespace, Resource
from http import HTTPStatus
from flask import request

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record.service.NRankRecordService import NRankRecordService
from domain.nrank_record_info.service.NRankRecordInfoService import NRankRecordInfoService
from domain.nrank_record.dto.NRankRecordCreateReqDto import NRankRecordCreateReqDto
from domain.nrank_record_info.dto.NRankRecordInfoCreateReqDto import NRankRecordInfoCreateReqDto
from domain.nrank_record.filter.NRankRecordSearchFilter import NRankRecordSearchFilter
from domain.page.PageableReqDto import PageableReqDto

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
        body = request.get_json()
        req_dto = NRankRecordCreateReqDto.IncludedKeywordAndMallName(body)

        nRankRecordService.create_one(req_dto.keyword, req_dto.mall_name)
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
    
@NRankRecordApi.route('/<record_id>/target:status/action:pending', methods=['PATCH'])
class NRankRecordChangeStatus(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE,
        WorkspaceAccessTypeEnum.STORE_RANK_CREATE
    })
    @transactional()
    def patch(self, record_id):
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
        body = request.get_json()
        req_dto = NRankRecordInfoCreateReqDto.IncludedRecordInfoId(body)
        
        nRankRecordService.change_status(record_id, NRankRecordStatusEnum.PENDING)
        nRankRecordInfoService.create_one(record_id, req_dto.record_info_id)
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
        body = request.get_json()
        record_req_dto = NRankRecordCreateReqDto.IncludedIds(body)

        nRankRecordInfoService = NRankRecordInfoService()
        body = request.get_json()
        record_info_req_dto = NRankRecordInfoCreateReqDto.IncludedRecordIds(body)
        
        nRankRecordService.change_list_status(record_req_dto.ids, NRankRecordStatusEnum.FAIL)
        nRankRecordInfoService.change_list_status_to_fail(record_info_req_dto.record_ids)
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
        body = request.get_json()
        req_dto = NRankRecordCreateReqDto.IncludedCategoryId(body)

        nRankRecordService.change_category_id(id, req_dto.nrank_record_category_id)
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
        params = {
            'search_condition': request.args.get('search_condition'),
            'search_query': request.args.get('search_query'),
            'search_category_id': request.args.get('search_category_id'),
            'search_status': request.args.get('search_status'),

            'sort_column': request.args.get('sort_column'),
            'sort_direction': request.args.get('sort_direction'),
            'page': request.args.get('page'),
            'size': request.args.get('size')
        }
        filter = NRankRecordSearchFilter(params)
        pageable = PageableReqDto.Size20To100(params)

        message.set_data(nRankRecordService.search_list_and_related_info(filter, pageable))
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
        params = {
            'search_condition': request.args.get('search_condition'),
            'search_query': request.args.get('search_query'),
            'search_category_id': request.args.get('search_category_id'),
            'search_status': request.args.get('search_status'),
        }
        filter = NRankRecordSearchFilter(params)

        message.set_data(nRankRecordService.search_list_count(filter))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code