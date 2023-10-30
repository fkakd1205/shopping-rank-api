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
        """create one for nrank record
        
        body : (NRankRecordCreateReqDto.IncludedKeywordAndMallName)
        - keyword
        - mall_name
        """
        message = MessageDto()
        
        nRankRecordService = NRankRecordService()
        body = request.get_json()
        req_dto = NRankRecordCreateReqDto.IncludedKeywordAndMallName(body)

        nRankRecordService.create_one(req_dto.keyword, req_dto.mall_name)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/<id>', methods=['DELETE'])
class NRankRecord(Resource):
    
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
    
@NRankRecordApi.route('/for:nrankSearchModal/action:searchStart', methods=['POST'])
class NRankRecord(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE,
        WorkspaceAccessTypeEnum.STORE_RANK_CREATE
    })
    @transactional()
    def post(self):
        """change nrank record status to pending & create one for nrank record info
        1. 랭킹 조회 횟수 검사
        2. change status
        3. create one for nrank record info (body로 전달받은 record info id 값 사용)

        body: (NRankRecordInfoCreateReqDto.IncludedRecordIdAndRecordInfoId)
        - record_id
        - record_info_id
        """
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        nRankRecordInfoService = NRankRecordInfoService()
        nRankRecordInfoService.check_allowed_search_count()
        body = request.get_json()
        req_dto = NRankRecordCreateReqDto.IncludedRecordIdAndRecordInfoId(body)
        
        nRankRecordService.change_status(req_dto.record_id, NRankRecordStatusEnum.PENDING)
        nRankRecordInfoService.create_one(req_dto.record_id, req_dto.record_info_id)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordApi.route('/target:status/action:fail', methods=['PATCH'])
class NRankRecord(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE,
        WorkspaceAccessTypeEnum.STORE_RANK_DELETE
    })
    @transactional()
    def patch(self):
        """change nrank records & related nrank record infos status to fail
        
        body: (NRankRecordInfoCreateReqDto.IncludedRecordIds)
        - record_ids
        """
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        body = request.get_json()
        record_req_dto = NRankRecordCreateReqDto.IncludedRecordIds(body)

        nRankRecordInfoService = NRankRecordInfoService()
        body = request.get_json()
        record_info_req_dto = NRankRecordInfoCreateReqDto.IncludedRecordIds(body)
        
        nRankRecordService.change_list_status(record_req_dto.record_ids, NRankRecordStatusEnum.FAIL)
        nRankRecordInfoService.change_list_status_to_fail(record_info_req_dto.record_ids)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordApi.route('/workspace-usage-info', methods=['GET'])
class NRankRecord(Resource):
    
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
class NRankRecord(Resource):
    
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
class NRankRecord(Resource):
    """search page for nrank record
    검색 조건에 따라 nrank record를 조회한다
    
    params: (NRankRecordSearchFilter), (PageableReqDto.Size20To100)
    - search_condition
    - search_query
    - search_category_id
    - search_status
    - sort_column
    - sort_direction
    - page
    - size
    """
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        params = request.args
        filter = NRankRecordSearchFilter(params)
        pageable = PageableReqDto.Size20To100(params)

        message.set_data(nRankRecordService.search_list_and_latest_info(filter, pageable))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordApi.route('/count', methods=['GET'])
class NRankRecord(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self):
        """search page for nrank record
        검색 조건에 따라 조회된 nrank record의 count를 반환한다
    
        params: (NRankRecordSearchFilter)
        - search_condition
        - search_query
        - search_category_id
        - search_status
        """
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        params = request.args
        filter = NRankRecordSearchFilter(params)

        message.set_data(nRankRecordService.search_list_count(filter))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code