from utils.type.CustomUTCDateTime import CustomUTCDateTime
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum
from dataclasses import dataclass

@dataclass
class NRankRecordDto():
    id = None
    keyword = None
    mall_name = None
    status = NRankRecordStatusEnum.NONE.value
    workspace_id = None
    created_at = None
    created_by_member_id = None
    current_nrank_record_info_id = None
    deleted_flag = None

    @staticmethod
    def to_dto(model):
        dto = NRankRecordDto()
        dto.id = model.id
        dto.keyword = model.keyword
        dto.mall_name = model.mall_name
        dto.status = model.status
        dto.workspace_id = model.workspace_id
        dto.created_at = CustomUTCDateTime.convert_timezone_format(model.created_at)
        dto.created_by_member_id = model.created_by_member_id
        dto.current_nrank_record_info_id = model.current_nrank_record_info_id
        dto.deleted_flag = model.deleted_flag
        return dto
    
    class RelatedNRankRecordInfos():
        def __init__(self, record_dto, record_info_dtos = []):
            self.id = record_dto.id
            self.keyword = record_dto.keyword
            self.mall_name = record_dto.mall_name
            self.status = record_dto.status
            self.workspace_id = record_dto.workspace_id
            self.created_at = record_dto.created_at
            self.created_by_member_id = record_dto.created_by_member_id
            self.current_nrank_record_info_id = record_dto.current_nrank_record_info_id
            self.deleted_flag = record_dto.deleted_flag
            
            self.infos = record_info_dtos
