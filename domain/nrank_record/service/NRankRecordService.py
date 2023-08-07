from flask import request
import uuid

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto

from utils.date.DateTimeUtils import DateTimeUtils
from exception.types.CustomException import *
from utils.db.v2.QueryUtils import transactional
from utils.user.UserUtils import UserUtils
from utils.workspace.MemberPermissionUtils import MemberPermissionUtils
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

class NRankRecordService():

    def check_duplication(self, dto):
        repository = NRankRecordRepository()

        model = repository.search_one_by_keyword_and_mall_name(dto.keyword, dto.mall_name, dto.workspace_id)
        if (model is not None):
            raise CustomDuplicationException("이미 등록된 데이터입니다.")
    
    @transactional
    def create_one(self):
        nrank_record_repository = NRankRecordRepository()
        dto = NRankRecordDto()
        
        body = request.get_json()
        workspace_id = MemberPermissionUtils().get_workspace_id()
        
        dto.id = uuid.uuid4()
        dto.keyword = body['keyword']
        dto.mall_name = body['mall_name']
        dto.status = NRankRecordStatusEnum.NONE.value
        dto.workspace_id = workspace_id
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = UserUtils().get_user_id_else_throw()
        dto.deleted_flag = False

        # keyword & mall_name 중복검사
        self.check_duplication(dto)
        
        new_model = NRankRecordModel.to_model(dto)
        nrank_record_repository.save(new_model)

    def search_list(self):
        """search list by workspace id

        1. nrank_record 조회
        2. nrank_record id 추출
        3. nrank_record_info 조회
        4. nrank_record infos에 nrank_record_info 매핑
        """
        nRankRecordRepository = NRankRecordRepository()
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        workspace_id = MemberPermissionUtils().get_workspace_id()

        record_models = nRankRecordRepository.search_list_by_workspace_id(workspace_id)
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
    
    def search_list_by_ids(self):
        """search list by ids and workspace id
        """
        nRankRecordRepository = NRankRecordRepository()
        workspace_id = MemberPermissionUtils().get_workspace_id()
        body = request.get_json()
        ids = body['ids']

        record_models = nRankRecordRepository.search_list_by_ids_and_workspace_id(ids, workspace_id)
        record_dtos = list(map(lambda model: NRankRecordDto.to_dto(model).__dict__, record_models))
        return record_dtos

    @transactional
    def delete_one(self, id):
        nRankRecordRepository = NRankRecordRepository()
        nRankRecordRepository.soft_delete_one_and_related_all(id)
    
    @transactional
    def change_status(self, id, status):
        nRankRecordRepository = NRankRecordRepository()
        record_model = nRankRecordRepository.search_one(id)
        if(record_model is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")
        record_model.status = status.value
