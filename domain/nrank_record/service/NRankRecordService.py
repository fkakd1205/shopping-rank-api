from flask import request
import uuid
from datetime import datetime

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from utils.date.DateTimeUtils import DateTimeUtils

class NRankRecordService():

    def create_one(self):
        repository = NRankRecordRepository()
        dto = NRankRecordDto()
        
        headers = request.headers
        body = request.get_json()
        
        dto.set_id(uuid.uuid4())
        dto.set_keyword(body['keyword'])
        dto.set_mall_name(body['mallName'])
        dto.set_workspace_id(headers['Wsid'])
        dto.set_created_at(DateTimeUtils.get_current_datetime())
        dto.set_created_by_member_id(uuid.UUID("212935ba-a222-40a6-8827-dcafedd3cd6c"))
                
        new_data = NRankRecordModel.to_entity(dto)
        repository.save(new_data)

    def search_list_by_workspace_id(self):
        repository = NRankRecordRepository()

        headers = request.headers
        entities = repository.search_list_by_workspace_id(headers['Wsid'])
        dtos = list(map(lambda entity: NRankRecordDto.to_dto(entity), entities))
        return dtos
    
    def search_one(self, id):
        repository = NRankRecordRepository()
        entity = repository.search_one(id)
        dto = NRankRecordDto.to_dto(entity)
        return dto
        

        

