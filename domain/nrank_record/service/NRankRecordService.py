from flask import request
import uuid

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto
from domain.nrank_record.dto.NRankWorkspaceUsageInfoDto import NRankWorkspaceUsageInfoDto
from domain.nrank_record_info.service.NRankRecordInfoService import NRankRecordInfoService

from utils import DateTimeUtils, MemberPermissionUtils
from exception.types.CustomException import *
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

from decorators import transactional

class NRankRecordService():

    @transactional
    def check_duplication(self, model):
        """check nrank record duplication in worksapce
        
        keyword & mall_name & workspace 가 동일한 경우 등록 제한
        """
        nrankRecordRepository = NRankRecordRepository()
        saved_model = nrankRecordRepository.search_one_by_keyword_and_mall_name(model.keyword, model.mall_name, model.workspace_id)
        if (saved_model):
            raise CustomDuplicationException("이미 등록된 데이터입니다.")
    
    @transactional
    def create_one(self):
        nrankRecordRepository = NRankRecordRepository()
        memberPermissionUtils = MemberPermissionUtils()

        body = request.get_json()
        workspace_info = memberPermissionUtils.get_workspace_info()
        
        dto = NRankRecordDto()
        dto.id = uuid.uuid4()
        dto.keyword = body['keyword']
        dto.mall_name = body['mall_name']
        dto.status = NRankRecordStatusEnum.NONE.value
        dto.status_updated_at = None
        dto.workspace_id = workspace_info.workspaceId
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = workspace_info.workspaceMemberId
        dto.current_nrank_record_info_id = None
        dto.deleted_flag = False

        new_model = NRankRecordModel.to_model(dto)

        # keyword & mall_name 중복검사
        self.check_duplication(new_model)
        nrankRecordRepository.save(new_model)

    @transactional
    def search_list(self):
        """search list by workspace id

        1. nrank_record 조회
        2. nrank_record id 추출
        3. nrank_record_info 조회
        4. nrank_record infos에 nrank_record_info 매핑
        """
        nRankRecordRepository = NRankRecordRepository()
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        memberPermissionUtils = MemberPermissionUtils()

        workspace_info = memberPermissionUtils.get_workspace_info()
        record_models = nRankRecordRepository.search_list_by_workspace_id(workspace_info.workspaceId)
        record_ids = list(map(lambda model: model.id, record_models))
        record_info_models = nRankRecordInfoRepository.search_list_by_record_ids(record_ids)

        record_related_record_info_dtos = self.set_record_and_related_record_infos(record_models, record_info_models)
        return record_related_record_info_dtos

    def set_record_and_related_record_infos(self, records, record_infos):
        """set nrank records related record infos
        
        records -- nrank records
        record_infos -- nrank records related nrank record infos
        """
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
    
    @transactional
    def change_status(self, id, status):
        """change status for nrank record
        
        id -- nrank record id
        status -- NRankRecordStatusEnum
        """
        
        nRankRecordRepository = NRankRecordRepository()
        current_datetime = DateTimeUtils.get_current_datetime()

        record_model = nRankRecordRepository.search_one(id)
        if(record_model is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")

        record_model.status = status.value
        record_model.status_updated_at = current_datetime

    @transactional
    def change_list_status(self, status):
        """change status for nrank records
        
        status -- NRankRecordStatusEnum
        body['ids'] -- nrank record id list
        """
        body = request.get_json()
        ids = body['ids']
        nRankRecordRepository = NRankRecordRepository()
        current_datetime = DateTimeUtils.get_current_datetime()

        record_models = nRankRecordRepository.search_list_by_ids(ids)
        if(record_models is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")
        
        for record_model in record_models:
            record_model.status = status.value
            record_model.status_updated_at = current_datetime

    @transactional
    def get_workspace_usage_info(self):
        nRankRecordInfoService = NRankRecordInfoService()
        memberPermissionUtils = MemberPermissionUtils()

        usage_info_dto = NRankWorkspaceUsageInfoDto()
        usage_info_dto.search_page_size = memberPermissionUtils.get_nrank_search_page_size()
        usage_info_dto.searched_count = nRankRecordInfoService.get_searched_count()
        usage_info_dto.allowed_search_count = memberPermissionUtils.get_nrank_allowed_search_count()
        return usage_info_dto.__dict__
