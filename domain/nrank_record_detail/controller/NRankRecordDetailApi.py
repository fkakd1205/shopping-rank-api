from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.nrank_record_detail.dto.NRankRecordDetailCreateReqDto import NRankRecordDetailCreateReqDto
from domain.nrank_record_detail.service.NRankRecordDetailServiceV2 import create_list
from domain.nrank_record_detail.service.NRankRecordDetailService import NRankRecordDetailService

from config.interceptor.RequiredLoginInterceptor import required_login

NRankRecordDetailApi = Namespace('NRankRecordDetailApi')

@NRankRecordDetailApi.route('/<record_id>', methods=['POST'])
class NRankRecordDetail(Resource):
    
    @required_login
    def post(self, record_id):
        message = MessageDto()

        # TODO :: page_size 설정하는 로직 추가
        page_size = 2
        create_req_dto = NRankRecordDetailCreateReqDto()
        create_req_dto.page_size = page_size
        create_req_dto.record_id = record_id
        # nRankRecordDetailService = NRankRecordDetailService()
        # nRankRecordDetailService.create_list(create_req_dto)
        # nRankRecordDetailService.create_list.apply_async(args=[create_req_dto.__dict__])
        # result = test.apply_async()

        # 실패 예외 핸들링
        # 실패 시 nrank record status - FAIL로 변경
        # 이 경우, create_list가 종료할 때 까지 response하지 않고 대기.
        # try:
        #     result = create_list.apply_async(args=[create_req_dto.__dict__])
        #     result.get()
        # except Exception as e:
        #     print("status change to Fail !!!!")
        #     nRankRecordService = NRankRecordService()
        #     nRankRecordService.change_status(record_id, NRankRecordStatusEnum.FAIL)
        #     return

        # result = create_list.apply_async(args=[create_req_dto.__dict__])
        
        # print(result.status)
        # if (result.status == 'FAILURE'):
        #     nRankRecordService = NRankRecordService()
        #     nRankRecordService.change_status(record_id, NRankRecordStatusEnum.FAIL)

        create_list.apply_async(args=[create_req_dto.__dict__])
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
        