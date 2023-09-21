from flask import request

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.repository.NRankRecordRepositoryV2 import NRankRecordRepositoryV2
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto
from domain.page.PageableReqDto import PageableReqDto
from domain.page.PageableResDto import PageableResDto
from domain.nrank_record.filter.NRankRecordSearchFilter import NRankRecordSearchFilter

from utils import MemberPermissionUtils
from exception.types.CustomException import *

from decorators import transactional

class NRankRecordServiceV2():
    
    @transactional(read_only=True)
    def search_list(self):
        """search list by workspace id

        1. nrank_record 조회
        2. nrank_record id 추출
        3. nrank_record_info 조회
        4. nrank_record infos에 nrank_record_info 매핑
        """
        nRankRecordRepository = NRankRecordRepositoryV2()
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        memberPermissionUtils = MemberPermissionUtils()
        workspace_info = memberPermissionUtils.get_workspace_info()
    
        params = {
            'search_condition': request.args.get('search_condition'),
            'search_query': request.args.get('search_query'),
            'search_category_id': request.args.get('search_category_id'),
            'search_status': request.args.get('search_status'),

            'sort_column': request.args.get('sort_column'),
            'sort_direction': request.args.get('sort_direction'),
            'page': request.args.get('page'),
            'size': request.args.get('size')
        }
        filter = NRankRecordSearchFilter(params)
        pageable = PageableReqDto.Size20To100(params)

        record_models = nRankRecordRepository.search_list_by_workspace_id_by_page(workspace_info.workspaceId, filter, pageable)
        record_ids = list(map(lambda model: model.id, record_models))
        record_info_models = nRankRecordInfoRepository.search_list_by_record_ids(record_ids)
        record_related_record_info_dtos = self.set_record_and_related_record_infos(record_models, record_info_models)

        res_dto = PageableResDto()
        res_dto.number = pageable.page - 1
        res_dto.size = pageable.size
        res_dto.content = record_related_record_info_dtos
        return res_dto.__dict__

    def set_record_and_related_record_infos(self, records, record_infos):
        """set nrank records related record infos
        
        - records : nrank records
        - record_infos : nrank records related nrank record infos
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

    @transactional(read_only=True)
    def search_list_count(self):
        nRankRecordRepository = NRankRecordRepositoryV2()
        memberPermissionUtils = MemberPermissionUtils()
        workspace_info = memberPermissionUtils.get_workspace_info()
    
        params = {
            'search_condition': request.args.get('search_condition'),
            'search_query': request.args.get('search_query'),
            'search_category_id': request.args.get('search_category_id'),
            'search_status': request.args.get('search_status'),
        }
        filter = NRankRecordSearchFilter(params)
        count = nRankRecordRepository.search_list_count_by_workspace_id(workspace_info.workspaceId, filter)
        res_dto = PageableResDto.TotalSize(count)
        return res_dto.__dict__