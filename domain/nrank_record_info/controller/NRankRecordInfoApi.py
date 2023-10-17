from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_info.service.NRankRecordInfoService import NRankRecordInfoService

from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from decorators import *

NRankRecordInfoApi = Namespace('NRankRecordInfoApi')

@NRankRecordInfoApi.route('/nrank-record/<record_id>', methods=['GET'])
class NRankRecordInfo(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.STORE_RANK_SEARCH
    })
    def get(self, record_id):
        message = MessageDto()

        nRankRecordInfoService = NRankRecordInfoService()
        message.set_data(nRankRecordInfoService.search_list(record_id))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
