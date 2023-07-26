from flask import request
import uuid

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModelV2 import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepositoryV2 import NRankRecordRepository
from domain.nrank_record_detail.repository.NRankRecordDetailRepositoryV2 import NRankRecordDetailRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepositoryV2 import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto

from utils.date.DateTimeUtils import DateTimeUtils
from exception.types.CustomException import CustomDuplicationException, CustomNotFoundException
from utils.db.v2.QueryUtils import transactional

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
        dto.deleted_flag = False

        # keyword & mall_name 중복검사
        self.check_duplication(dto)
        
        new_model = NRankRecordModel.to_model(dto)
        repository.save(new_model)
        """"""

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
        
    # deprecated
    # def search_one(self, id):
    #     repository = NRankRecordRepository()

    #     entity = repository.search_one(id)
    #     dto = NRankRecordDto.to_dto(entity)
    #     return dto
    
    # deprecated
    # def delete_one(self, id):
    #     nRankRecordRepository = NRankRecordRepository()
    #     nRankRecordDetailRepository = NRankRecordDetailRepository()
    #     nRankRecordInfoRepository = NRankRecordInfoRepository()

    #     # TODO :: search_one 제거
    #     model = nRankRecordRepository.search_one(id)
    #     if (model is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")
    #     nRankRecordRepository.delete_one_by_id(model.id)

    #     info_models = nRankRecordInfoRepository.search_list_by_record_id(model.id)
    #     info_ids = list(map(lambda info: info.id, info_models))
    #     nRankRecordDetailRepository.bulk_delete_by_record_info_ids(info_ids)
    #     nRankRecordInfoRepository.bulk_delete_by_ids(info_ids)

    @transactional
    def delete_one(self, id):
        nRankRecordRepository = NRankRecordRepository()
        nRankRecordRepository.deleted_one_related_nrank_record_info_and_nrank_recrod_detail(id)
    