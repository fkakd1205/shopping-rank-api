from flask_restx import Namespace, Resource
from http import HTTPStatus
import threading

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_detail.dto.NRankRecordDetailCreateReqDto import NRankRecordDetailCreateReqDto
from domain.nrank_record_detail.service.NRankRecordDetailServiceV2 import NRankRecordDetailService
from utils import MemberPermissionUtils

from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum

from decorators import *

NRankRecordDetailApi = Namespace('NRankRecordDetailApi')

@NRankRecordDetailApi.route('/<record_id>', methods=['POST'])
class NRankRecordDetail(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def post(self, record_id):
        message = MessageDto()

        nrankRecordDetailService = NRankRecordDetailService()
        memberPermissionUtils = MemberPermissionUtils()
        page_size = memberPermissionUtils.get_nrank_search_page_size()

        create_req_dto = NRankRecordDetailCreateReqDto()
        create_req_dto.page_size = page_size
        create_req_dto.record_id = record_id

        # TODO :: searched_count 검사
        threading.Thread(target=nrankRecordDetailService.create_list, args=(create_req_dto.__dict__, ), daemon=True).start()
        
        message.set_status(HTTPStatus.ACCEPTED)
        message.set_message("accepted")

        return message.__dict__, message.status_code
    
@NRankRecordDetailApi.route('/nrank-record-info/<record_info_id>', methods=['GET'])
class NRankRecordDetailIncludeNRankRecordInfoId(Resource):

    @required_login
    def get(self, record_info_id):
        message = MessageDto()

        nRankRecordDetailService = NRankRecordDetailService()
        message.set_data(nRankRecordDetailService.search_list_by_record_info_id(record_info_id))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
        