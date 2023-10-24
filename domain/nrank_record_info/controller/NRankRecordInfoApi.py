from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_info.service.NRankRecordInfoService import NRankRecordInfoService

from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from decorators import *

NRankRecordInfoApi = Namespace('NRankRecordInfoApi')

INFO_LIMIT_SIZE_FOR_NRARNK_SEARCH_MODAL = 20

@NRankRecordInfoApi.route('/for:nrankSearchModal/nrank-record/<record_id>', methods=['GET'])
class NRankRecordInfo(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self, record_id):
        """search limit list for nrank record info
        nrankSearchModal에서 사용되는 특정 api
        
        params:
        - record_id
        """
        message = MessageDto()

        nRankRecordInfoService = NRankRecordInfoService()
        limit_size = INFO_LIMIT_SIZE_FOR_NRARNK_SEARCH_MODAL
        
        message.set_data(nRankRecordInfoService.search_list_by_record_id(record_id, limit_size))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
