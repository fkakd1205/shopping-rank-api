from flask_restx import Namespace, Resource
from http import HTTPStatus
import asyncio

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_detail.service.NRankRecordDetailServiceV3 import NRankRecordDetailService

NRankRecordDetailApi = Namespace('NRankRecordDetail')

@NRankRecordDetailApi.route('/<record_id>', methods=['POST'])
class NRankRecordDetail(Resource):
    def post(self, record_id):
        message = MessageDto()

        # TODO :: page_size 구하는 로직 추가
        page_size = 2
        nRankRecordDetailService = NRankRecordDetailService(page_size, record_id)
        nRankRecordDetailService.create_list()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordDetailApi.route('/nrank-record-info/<record_info_id>', methods=['GET'])
class NRankRecordDetailIncludeNRankRecordInfoId(Resource):
    def get(self, record_info_id):
        message = MessageDto()

        nRankRecordDetailService = NRankRecordDetailService()
        message.set_data(nRankRecordDetailService.search_list_by_record_info_id(record_info_id))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
        