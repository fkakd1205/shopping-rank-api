from flask import request
import uuid

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto

from utils.date.DateTimeUtils import DateTimeUtils
from exception.types.CustomException import CustomDuplicationException
from utils.db.v2.QueryUtils import transactional
from utils.user.UserUtils import UserUtils

class NRankRecordService():

    def check_duplication(self, dto):
        """check duplication for keyword & mall_name
        
        Keyword arguments:
        dto -- NRankRecordDto
        """
        repository = NRankRecordRepository()

        model = repository.search_one_by_keyword_and_mall_name(dto.keyword, dto.mall_name)
        if (model is not None):
            raise CustomDuplicationException("이미 등록된 데이터입니다.")
    
    @transactional
    def create_one(self):
        """create one
        
        Use Service Method:
            self.check_duplication
        Use Repository Method:
            NRankRecordRepository -- save
        """
        nrank_record_repository = NRankRecordRepository()
        dto = NRankRecordDto()
        
        headers = request.headers
        body = request.get_json()
        
        dto.id = uuid.uuid4()
        dto.keyword = body['keyword']
        dto.mall_name = body['mall_name']
        dto.workspace_id = headers['wsId']
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = UserUtils().get_user_id_else_throw()
        dto.deleted_flag = False

        # keyword & mall_name 중복검사
        self.check_duplication(dto)
        
        new_model = NRankRecordModel.to_model(dto)
        nrank_record_repository.save(new_model)

    def search_list_by_workspace_id(self):
        """search list by workspace id
        1. nrank_record 조회
        2. nrank_record id 추출
        3. nrank_record_info 조회
        4. nrank_record infos에 nrank_record_info 매핑

        Return: 
            NRankRecordDto.RelatedNRankRecordInfos
        Use Repository Method:
            NRankRecordRepository -- search_list_by_workspace_id
            NRankRecordInfoRepository -- search_list_by_record_ids
        Use Service Method:
            self.set_record_and_related_record_infos
        """
        nRankRecordRepository = NRankRecordRepository()
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        headers = request.headers

        record_models = nRankRecordRepository.search_list_by_workspace_id(headers['wsId'])
        record_ids = list(map(lambda model: model.id, record_models))
        record_info_models = nRankRecordInfoRepository.search_list_by_record_ids(record_ids)
    
        record_related_record_info_dtos = self.set_record_and_related_record_infos(record_models, record_info_models)
        return record_related_record_info_dtos

    def set_record_and_related_record_infos(self, records, record_infos):
        dtos = []
        record_info_dtos = list(map(lambda model: NRankRecordInfoDto.to_dto(model), record_infos))

        for record in records:
            record_dto = NRankRecordDto.to_dto(record)
            infos = []
            for record_info_dto in record_info_dtos:
                if(record_dto.id == record_info_dto.nrank_record_id):
                    infos.append(record_info_dto.__dict__)
                
            dtos.append(NRankRecordDto.RelatedNRankRecordInfos(record_dto, infos).__dict__)

        return dtos

    @transactional
    def delete_one(self, id):
        nRankRecordRepository = NRankRecordRepository()
        nRankRecordRepository.soft_delete_one_and_related_all(id)
    