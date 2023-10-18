from flask_restx import Namespace, Resource
from http import HTTPStatus
import threading
from flask import request

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_detail.dto.NRankRecordDetailCreateReqDto import NRankRecordDetailCreateReqDto
from domain.nrank_record_detail.service.NRankRecordDetailService import NRankRecordDetailService
from domain.nrank_record_detail.dto.NRankRecordDetailSearchReqDto import NRankRecordDetailSearchReqDto

from utils import MemberPermissionUtils
from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from decorators import *
from config.server.ServerConfig import config
from exception.types.CustomException import *

NRankRecordDetailApi = Namespace('NRankRecordDetailApi')

@NRankRecordDetailApi.route('', methods=['POST'])
class NRankRecordDetail(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    @transactional(read_only=True)
    def post(self):
        """네이버 쇼핑 랭킹 요청 항목 세팅 및 응답 결과를 저장하는 api 요청
        
        NRankRecordDetailService : nrank_request_setting => 네이버 쇼핑 랭킹 요청 시 필요한 항목들 세팅
        NRankRecordDetailService : request_nrank => 네이버 쇼핑 랭킹 api 요청 및 조회 결과를 저장하는 api 요청
        """
        message = MessageDto()

        nrankRecordDetailService = NRankRecordDetailService()
        memberPermissionUtils = MemberPermissionUtils()
        workspace_info = memberPermissionUtils.get_workspace_info()
        page_size = memberPermissionUtils.get_nrank_search_page_size()

        body = request.get_json()
        search_req_dto = NRankRecordDetailSearchReqDto.IncludedRecordIdAndRecordInfoId(body)

        search_req_dto = {
            'page_size': page_size,
            'record_id': search_req_dto.record_id,
            'record_info_id': search_req_dto.record_info_id,
            'workspace_id': workspace_info.workspaceId
        }
        create_req_dto = NRankRecordDetailCreateReqDto.RequestNRank(search_req_dto)

        req_dto = nrankRecordDetailService.nrank_request_setting(create_req_dto)
        threading.Thread(target=nrankRecordDetailService.request_nrank, args=(req_dto.__dict__, request.cookies), daemon=True).start()
        message.set_status(HTTPStatus.ACCEPTED)
        message.set_message("accepted")

        return message.__dict__, message.status_code
    
@NRankRecordDetailApi.route('/nrank-record-info/<record_info_id>', methods=['GET'])
class NRankRecordDetailIncludeNRankRecordInfoId(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self, record_info_id):
        message = MessageDto()

        nRankRecordDetailService = NRankRecordDetailService()
        message.set_data(nRankRecordDetailService.search_list_by_record_info_id(record_info_id))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code

@NRankRecordDetailApi.route('/results', methods=['POST'])
class NRankRecordDetail(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH,
        WorkspaceAccessTypeEnum.STORE_RANK_CREATE,
        WorkspaceAccessTypeEnum.STORE_RANK_UPDATE
    })
    def post(self):
        """랭킹 조회 결과를 저장하는 api
        
        1. direct access key 값 검사
        2. nrank record detail 저장
        """
        message = MessageDto()

        # 1.
        check_nrank_direct_key()

        # 2.
        nrankRecordDetailService = NRankRecordDetailService()
        nrankRecordDetailService.create_list()
        message.set_status(HTTPStatus.ACCEPTED)
        message.set_message("accepted")

        return message.__dict__, message.status_code
    
def check_nrank_direct_key():
    try:
        server_ac_key = config['nrankDirectAccessKey']
        origin_ac_key = request.headers['nrankDirectAccessKey']

        if(server_ac_key is None or origin_ac_key is None):
            raise
        if(server_ac_key != origin_ac_key):
            raise
    except:
        raise CustomMethodNotAllowedException("거부된 요청입니다.")
        
@NRankRecordDetailApi.route('/search', methods=['POST'])
class NRankRecordDetail(Resource):
    
    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def post(self):
        message = MessageDto()

        nrankRecordDetailService = NRankRecordDetailService()
        message.set_data(nrankRecordDetailService.search_list_by_filter())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code