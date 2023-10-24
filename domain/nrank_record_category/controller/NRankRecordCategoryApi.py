from flask_restx import Namespace, Resource
from http import HTTPStatus
from flask import request

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_category.service.NRankRecordCategoryService import NRankRecordCategoryService
from domain.nrank_record_category.dto.NRankRecordCategoryCreateReqDto import NRankRecordCategoryCreateReqDto

from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from decorators import *

NRankRecordCategoryApi = Namespace('NRankRecordCategoryApi')

@NRankRecordCategoryApi.route('', methods=['GET', 'POST'])
class NRankRecordCategory(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self):
        message = MessageDto()

        nRankRecordCategoryService = NRankRecordCategoryService()

        message.set_data(nRankRecordCategoryService.search_list())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_CREATE
    })
    def post(self):
        message = MessageDto()

        nRankRecordCategoryService = NRankRecordCategoryService()
        body = request.get_json()
        req_dto = NRankRecordCategoryCreateReqDto.IncludedName(body)

        nRankRecordCategoryService.create_one(req_dto.name)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordCategoryApi.route('/<id>', methods=['PUT', 'DELETE'])
class NRankRecordCategory(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE
    })
    def put(self, id):
        message = MessageDto()

        nRankRecordCategoryService = NRankRecordCategoryService()
        body = request.get_json()
        req_dto = NRankRecordCategoryCreateReqDto.IncludedName(body)

        nRankRecordCategoryService.update_one(id, req_dto.name)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_DELETE
    })
    def delete(self, id):
        message = MessageDto()

        nRankRecordCategoryService = NRankRecordCategoryService()
        nRankRecordCategoryService.delete_one(id)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
