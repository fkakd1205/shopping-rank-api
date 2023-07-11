from flask_restx import Namespace, Resource
from http import HTTPStatus
import asyncio

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_detail.service.NRankRecordDetailService import NRankRecordDetailService

NRankRecordDetailApi = Namespace('NRankRecordDetail')

@NRankRecordDetailApi.route('', methods=['POST'])
class NRankRecordDetail(Resource):
    def post(self):
        message = MessageDto()

        # TODO :: page_size 구하는 로직 추가
        page_size = 2
        nRankRecordDetailService = NRankRecordDetailService(page_size)
        asyncio.run(nRankRecordDetailService.create_list())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
@NRankRecordDetailApi.route('/nrank-records/<record_id>', methods=['GET'])
class NRankRecordDetailIncludeNRankRecordId(Resource):
    def get(self, record_id):
        message = MessageDto()

        nRankRecordDetailService = NRankRecordDetailService()
        message.set_data(nRankRecordDetailService.search_list_by_record_id(record_id))
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
        