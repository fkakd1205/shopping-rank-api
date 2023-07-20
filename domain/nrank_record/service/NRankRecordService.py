from flask import request
import uuid

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepositoryV3 import NRankRecordRepository
from domain.nrank_record_detail.repository.NRankRecordDetailRepositoryV2 import NRankRecordDetailRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto

from utils.date.DateTimeUtils import DateTimeUtils
from exception.types.CustomDuplicationException import CustomDuplicationException

class NRankRecordService():

    def check_duplication(self, dto):
        repository = NRankRecordRepository()

        entity = repository.search_one_by_keyword_and_mall_name(dto.keyword, dto.mall_name)
        if(entity is not None) :
            raise CustomDuplicationException("이미 등록된 데이터입니다.")
        
    def create_one(self):
        repository = NRankRecordRepository()
        dto = NRankRecordDto()
        
        headers = request.headers
        body = request.get_json()
        
        dto.id = uuid.uuid4()
        dto.keyword = body['keyword']
        dto.mall_name = body['mall_name']
        dto.workspace_id = headers['wsId']
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = uuid.UUID("212935ba-a222-40a6-8827-dcafedd3cd6c")

        # keyword & mall_name 중복검사
        self.check_duplication(dto)
        
        new_model = NRankRecordModel.to_model(dto)
        repository.save(new_model)

    def search_list_by_workspace_id(self):
        repository = NRankRecordRepository()
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        headers = request.headers

        '''
        1. nrank_record 조회
        2. nrank_record id 추출
        3. nrank_record_info 조회
        4. nrank_record infos에 nrank_record_info 매핑
        '''
        record_models = repository.search_list_by_workspace_id(headers['wsId'])
        record_ids = list(map(lambda model: model.id, record_models))
        record_info_models = nRankRecordInfoRepository.searh_list_by_record_ids(record_ids)

        record_related_record_info = []
        for record in record_models:
            record_dto = NRankRecordDto.to_dto(record)
            
            infos = []
            for record_info in record_info_models:
                if(record.id == record_info.nrank_record_id):
                    infos.append(NRankRecordInfoDto.to_dto(record_info))

            record_dto['infos'] = infos
            record_related_record_info.append(record_dto)

        return record_related_record_info
        
    def search_one(self, id):
        repository = NRankRecordRepository()

        entity = repository.search_one(id)
        dto = NRankRecordDto.to_dto(entity)
        return dto
    
    def deleteOne(self, id):
        repository = NRankRecordRepository()
        nrankRecordRepository = NRankRecordDetailRepository()
        nRankRecordInfoRepository = NRankRecordInfoRepository()

        # TODO :: 예외처리하기
        entity = repository.search_one(id)
        repository.delete_one(entity)
        nrankRecordRepository.bulk_delete(entity.id)
        nRankRecordInfoRepository.bulk_delete(entity.id)        
        
    