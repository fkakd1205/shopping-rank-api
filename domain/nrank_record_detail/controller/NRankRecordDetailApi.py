from flask_restx import Namespace, Resource
from http import HTTPStatus
import threading
from flask import request

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_detail.dto.NRankRecordDetailCreateReqDto import NRankRecordDetailCreateReqDto
from domain.nrank_record_detail.service.NRankRecordDetailServiceV2 import NRankRecordDetailService

from utils import MemberPermissionUtils
from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from decorators import *

NRankRecordDetailApi = Namespace('NRankRecordDetailApi')

@NRankRecordDetailApi.route('', methods=['POST'])
class NRankRecordDetail(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def post(self):
        message = MessageDto()

        nrankRecordDetailService = NRankRecordDetailService()
        memberPermissionUtils = MemberPermissionUtils()
        page_size = memberPermissionUtils.get_nrank_search_page_size()

        body = request.get_json()
        record_id = body['record_id']
        record_info_id = body['record_info_id']

        create_req_dto = NRankRecordDetailCreateReqDto()
        create_req_dto.page_size = page_size
        create_req_dto.record_id = record_id
        create_req_dto.record_info_id = record_info_id

        threading.Thread(target=nrankRecordDetailService.create_list, args=(create_req_dto.__dict__, ), daemon=True).start()
        message.set_status(HTTPStatus.ACCEPTED)
        message.set_message("accepted")

        return message.__dict__, message.status_code
    
@NRankRecordDetailApi.route('/nrank-record-info/<record_info_id>', methods=['GET'])
class NRankRecordDetailIncludeNRankRecordInfoId(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def get(self, record_info_id):
        message = MessageDto()

        nRankRecordDetailService = NRankRecordDetailService()
        message.set_data(nRankRecordDetailService.search_list_by_record_info_id(record_info_id))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
        