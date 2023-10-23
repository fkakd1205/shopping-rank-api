import uuid

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from domain.nrank_record.repository.NRankRecordSearchPagingRepository import NRankRecordSearchPagingRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto
from domain.nrank_record.dto.NRankWorkspaceUsageInfoDto import NRankWorkspaceUsageInfoDto
from domain.nrank_record_info.service.NRankRecordInfoService import NRankRecordInfoService
from domain.page.PageableResDto import PageableResDto

from utils import DateTimeUtils, MemberPermissionUtils
from exception.types.CustomException import *
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

from decorators import transactional

class NRankRecordService():

    @transactional(read_only=True)
    def check_duplication(self, dto):
        """check nrank record duplication in worksapce
        
        keyword & mall_name & workspace 가 동일한 경우 등록 제한
        """
        nrankRecordRepository = NRankRecordRepository()
        saved_model = nrankRecordRepository.search_one_by_keyword_and_mall_name(dto.keyword, dto.mall_name, dto.workspace_id)
        if (saved_model):
            raise CustomDuplicationException("이미 등록된 데이터입니다.")

    @transactional()
    def create_one(self, keyword, mall_name):
        nrankRecordRepository = NRankRecordRepository()
        memberPermissionUtils = MemberPermissionUtils()
        workspace_info = memberPermissionUtils.get_workspace_info()

        dto = NRankRecordDto()
        dto.id = uuid.uuid4()
        dto.keyword = (keyword or '').strip()
        dto.mall_name = (mall_name or '').strip()
        dto.status = NRankRecordStatusEnum.NONE.value
        dto.status_updated_at = None
        dto.workspace_id = workspace_info.workspaceId
        dto.nrank_record_category_id = None
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = workspace_info.workspaceMemberId
        dto.current_nrank_record_info_id = None
        dto.deleted_flag = False

        self.check_format(dto)
        self.check_duplication(dto)
        new_model = NRankRecordModel.to_model(dto)
        nrankRecordRepository.save(new_model)

    def check_format(self, dto):
        if(dto.keyword == ''):
            raise CustomNotMatchedFormatException("키워드는 공백이 불가능합니다.")

        if(len(dto.keyword) > 50):
            raise CustomNotMatchedFormatException("키워드는 50글자 이하로 입력해주세요.")    
        
        if(dto.mall_name == ''):
            raise CustomNotMatchedFormatException("스토어명은 공백이 불가능합니다.")
        
        if(len(dto.mall_name) > 50):
            raise CustomNotMatchedFormatException("스토어명은 50글자 이하로 입력해주세요.")
    
    @transactional(read_only=True)
    def search_list_and_related_info(self, filter, pageable):
        """search list by workspace id

        1. nrank_record 조회
        2. nrank_record id 추출
        3. nrank_record_info 조회 - 조회가 성공적으로 완료되었으며, 삭제되지 않은 info
        4. nrank_record의 nrank_record_info필드에 nrank_record_info 매핑
        5. PageableResDto 세팅

        Return
        - PagealbeResDto
        """
        nRankRecordSearchPagingRepository = NRankRecordSearchPagingRepository()
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        memberPermissionUtils = MemberPermissionUtils()
        workspace_info = memberPermissionUtils.get_workspace_info()

        record_models = nRankRecordSearchPagingRepository.search_list_by_page(workspace_info.workspaceId, filter, pageable)
        record_ids = list(map(lambda model: model.id, record_models))
        record_info_models = nRankRecordInfoRepository.search_list_by_record_ids(record_ids)
        record_related_record_info_dto = self.set_record_and_related_current_record_info(record_models, record_info_models)

        res_dto = PageableResDto()
        res_dto.number = pageable.page - 1
        res_dto.size = pageable.size
        res_dto.content = record_related_record_info_dto
        return res_dto.__dict__
    
    def set_record_and_related_current_record_info(self, records, record_infos):
        """set nrank records related currnet record info
        
        - records : nrank records
        - record_info : nrank records related current nrank record info
        """
        dtos = []
        record_info_dtos = list(map(lambda model: NRankRecordInfoDto.to_dto(model), record_infos))

        for record in records:
            record_dto = NRankRecordDto.to_dto(record)
            info = None

            for record_info_dto in record_info_dtos:
                if(record_dto.id == record_info_dto.nrank_record_id):
                    info = record_info_dto.__dict__

            dtos.append(NRankRecordDto.RelatedCurrentNRankRecordInfo(record_dto, info).__dict__)
        return dtos

    @transactional(read_only=True)
    def search_list_count(self, filter) -> (PageableResDto.TotalSize):
        """search list count
        
        Return
        - PageableResDto.TotalSize
        """
        nRankRecordSearchPagingRepository = NRankRecordSearchPagingRepository()
        memberPermissionUtils = MemberPermissionUtils()
        workspace_info = memberPermissionUtils.get_workspace_info()
    
        count = nRankRecordSearchPagingRepository.search_list_count_by_workspace_id(workspace_info.workspaceId, filter)
        res_dto = PageableResDto.TotalSize(count)
        return res_dto.__dict__

    @transactional()
    def delete_one(self, id):
        """delete nrank record
        
        - delete nrank record
        - delete related nrank record info
        - delete related nrank record details
        """
        nRankRecordRepository = NRankRecordRepository()
        nRankRecordRepository.soft_delete_one_and_related_all(id)
    
    @transactional()
    def change_status(self, id, status):
        """change status for nrank record
        
        - id : nrank record id
        - status : NRankRecordStatusEnum
        """
        nRankRecordRepository = NRankRecordRepository()
        current_datetime = DateTimeUtils.get_current_datetime()

        record_model = nRankRecordRepository.search_one(id)
        if(record_model is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")

        record_model.status = status.value
        record_model.status_updated_at = current_datetime

    @transactional()
    def change_list_status(self, ids, status):
        """change status for nrank records
        
        - status : NRankRecordStatusEnum
        - NRankRecordCreateReqDto : nrank record id list
        """
        nRankRecordRepository = NRankRecordRepository()
        current_datetime = DateTimeUtils.get_current_datetime()

        record_models = nRankRecordRepository.search_list_by_ids(ids)
        if(record_models is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")
        
        for record_model in record_models:
            record_model.status = status.value
            record_model.status_updated_at = current_datetime

    @transactional(read_only=True)
    def get_workspace_usage_info(self):
        nRankRecordInfoService = NRankRecordInfoService()
        memberPermissionUtils = MemberPermissionUtils()

        usage_info_dto = NRankWorkspaceUsageInfoDto()
        usage_info_dto.search_page_size = memberPermissionUtils.get_nrank_search_page_size()
        usage_info_dto.searched_count = nRankRecordInfoService.get_searched_count()
        usage_info_dto.allowed_search_count = memberPermissionUtils.get_nrank_allowed_search_count()
        return usage_info_dto.__dict__

    @transactional()
    def change_category_id(self, id, category_id):
        nRankRecordRepository = NRankRecordRepository()

        record_model = nRankRecordRepository.search_one(id)
        if(record_model is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")

        record_model.nrank_record_category_id = category_id
