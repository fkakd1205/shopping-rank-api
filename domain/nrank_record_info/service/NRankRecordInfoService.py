from domain.nrank_record_info.model.NRankRecordInfoModel import NRankRecordInfoModel
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto

from decorators import *
from utils import *
from exception.types.CustomException import * 
from enums.NRankRecordInfoStatusEnum import NRankRecordInfoStatusEnum

class NRankRecordInfoService():
    
    @transactional()
    def create_one(self, record_id, record_info_id):
        nrankRecordInfoRepository = NRankRecordInfoRepository()
        current_datetime = DateTimeUtils.get_current_datetime()

        record_info_model = nrankRecordInfoRepository.search_one(record_info_id)
        if(record_info_model):
            raise CustomDuplicationException("요청이 중복되었습니다. 잠시 후 다시 시도해주세요.")

        dto = NRankRecordInfoDto()
        dto.id = record_info_id
        dto.status = NRankRecordInfoStatusEnum.NONE.value
        dto.created_at = current_datetime
        dto.nrank_record_id = record_id
        dto.deleted_flag = False
        new_model = NRankRecordInfoModel.to_model(dto)
        nrankRecordInfoRepository.save(new_model)
    
    @transactional()
    def change_list_status_to_fail(self, record_ids):
        fail_status = NRankRecordInfoStatusEnum.FAIL.value
        nRankRecordInfoRepository = NRankRecordInfoRepository()

        record_info_models = nRankRecordInfoRepository.search_list_by_record_ids(record_ids)
        if(record_info_models is None): return
        
        fail_info_model = list(filter(lambda info: info.status == NRankRecordInfoStatusEnum.NONE.value, record_info_models))

        for record_info in fail_info_model:
            record_info.status = fail_status
            record_info.deleted_flag = True

    @transactional(read_only=True)
    def check_allowed_search_count(self):
        memberUtils = MemberPermissionUtils()
        searched_cnt = self.get_searched_count()

        allowed_search_cnt = memberUtils.get_nrank_allowed_search_count()
        if(searched_cnt >= allowed_search_cnt):
            raise CustomMethodNotAllowedException("금일 요청 가능한 횟수를 초과했습니다.")
        
    @transactional(read_only=True)
    def get_searched_count(self):
        memberUtils = MemberPermissionUtils()
        nrankRecordInfoRepository = NRankRecordInfoRepository()
        workspace_info = memberUtils.get_workspace_info()
        ws_id = workspace_info.workspaceId

        date = DateTimeUtils.get_current_datetime()
        start_date = DateTimeUtils.get_utc_start_date(date)
        end_date = DateTimeUtils.get_utc_end_date(date)
        searched_cnt = nrankRecordInfoRepository.search_count_by_period_and_workspace_id(start_date, end_date, ws_id)
        return searched_cnt
    
    # TODO :: 추후에 limit_size가 필요없는 api가 필요한 경우 다음과 같이 작성
    # @transactional(read_only=True)
    # def search_list_by_record_id(self, record_id):
    #     nRankRecordInfoRepository = NRankRecordInfoRepository()
    #     info_models = nRankRecordInfoRepository.search_list_by_record_id(record_id,)
    #     info_dtos = list(map(lambda model: NRankRecordInfoDto.to_dto(model).__dict__, info_models))
    #     return info_dtos
    
    @transactional(read_only=True)
    def search_list_by_record_id(self, record_id, limit_size):
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        info_models = nRankRecordInfoRepository.search_limit_list_by_record_id(record_id, limit_size)
        info_dtos = list(map(lambda model: NRankRecordInfoDto.to_dto(model).__dict__, info_models))
        return info_dtos
