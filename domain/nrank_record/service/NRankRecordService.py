from flask import request
import uuid

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from domain.nrank_record.sub_domain.nrank_record_detail.repository.NRankRecordDetailOfNRankRecordRepository import NRankRecordDetailOfNRankRecordRepository

from utils.date.DateTimeUtils import DateTimeUtils
from exception.types.CustomDuplicationException import CustomDuplicationException

class NRankRecordService():

    def create_one(self):
        repository = NRankRecordRepository()
        dto = NRankRecordDto()
        
        headers = request.headers
        body = request.get_json()
        
        dto.id = uuid.uuid4()
        dto.keyword = body['keyword']
        dto.mall_name = body['mall_name']
        dto.workspace_id = headers['Wsid']
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = uuid.UUID("212935ba-a222-40a6-8827-dcafedd3cd6c")

        self.check_duplication(dto)
        
        new_entity = NRankRecordModel.to_entity(dto)
        repository.save(new_entity)

    def search_list_by_workspace_id(self):
        repository = NRankRecordRepository()

        headers = request.headers
        entities = repository.search_list_by_workspace_id(headers['Wsid'])
        dtos = list(map(lambda entity: NRankRecordDto.to_dto(entity), entities))
        return dtos
    
    def check_duplication(self, dto):
        repository = NRankRecordRepository()

        entity = repository.search_one_by_keyword_and_mall_name(dto.keyword, dto.mall_name)
        if(entity is not None) :
            raise CustomDuplicationException("이미 등록된 데이터입니다.")

    def search_one(self, id):
        repository = NRankRecordRepository()

        entity = repository.search_one(id)
        dto = NRankRecordDto.to_dto(entity)
        return dto
    
    def deleteOne(self, id):
        repository = NRankRecordRepository()
        nrankRecordRepository = NRankRecordDetailOfNRankRecordRepository()

        entity = repository.search_one(id)
        repository.delete_one(entity)
        nrankRecordRepository.bulk_delete(entity.id)
        
    