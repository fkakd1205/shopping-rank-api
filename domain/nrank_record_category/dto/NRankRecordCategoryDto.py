from utils import CustomUTCDateTime
from dataclasses import dataclass

@dataclass
class NRankRecordCategoryDto():
    id = None
    name = None
    created_at = None
    updated_at = None
    created_by_member_id = None
    deleted_flag = None
    workspace_id = None

    @staticmethod
    def to_dto(model):
        dto = NRankRecordCategoryDto()
        dto.id = model.id
        dto.name = model.name
        dto.created_at = CustomUTCDateTime.convert_timezone_format(model.created_at)
        dto.updated_at = CustomUTCDateTime.convert_timezone_format(model.updated_at)
        dto.created_by_member_id = model.created_by_member_id
        dto.deleted_flag = model.deleted_flag
        dto.workspace_id = model.workspace_id
        return dto.__dict__