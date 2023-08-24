import uuid

from domain.nrank_record_info.model.NRankRecordInfoModel import NRankRecordInfoModel
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository

from decorators import *
from utils import *
from enums.NRankRecordInfoStatusEnum import NRankRecordInfoStatusEnum

class NRankRecordInfoService():
    
    @transactional
    def create_one_and_get_id(self, record_id):
        nrankRecordInfoRepository = NRankRecordInfoRepository()
        current_datetime = DateTimeUtils.get_current_datetime()

        info_id = uuid.uuid4()
        record_info_model = NRankRecordInfoModel()
        record_info_model.id = info_id
        record_info_model.status = NRankRecordInfoStatusEnum.NONE.value
        record_info_model.created_at = current_datetime
        record_info_model.nrank_record_id = record_id
        record_info_model.deleted_flag = False
        nrankRecordInfoRepository.save(record_info_model)
        return str(info_id)
    
    @transactional
    def change_list_status_to_fail(self):
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        record_infos = nRankRecordInfoRepository.search_list_by_status(NRankRecordInfoStatusEnum.NONE)
        fail_status = NRankRecordInfoStatusEnum.FAIL.value

        for record_info in record_infos:
            record_info.status = fail_status
            record_info.deleted_flag = True
