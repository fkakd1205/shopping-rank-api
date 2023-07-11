from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record.service.NRankRecordService import NRankRecordService

NRankRecordApi = Namespace('NRankRecordApi')

@NRankRecordApi.route('', methods=['GET', 'POST'])
class NRankRecord(Resource):
    def post(self):
        message = MessageDto()
        
        nRankRecordService = NRankRecordService()
        nRankRecordService.create_one()
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    
    def get(self):
        message = MessageDto()

        nRankRecordService = NRankRecordService()
        message.set_data(nRankRecordService.search_list_by_workspace_id())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code
    