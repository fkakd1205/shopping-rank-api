from utils.type.CustomUTCDateTime import CustomUTCDateTime
from dataclasses import dataclass

@dataclass
class NRankRecordInfoDto():
    id = None
    thumbnail_url = None
    rank_detail_unit = None
    ad_rank_detail_unit = None
    created_at = None
    nrank_record_id = None
    deleted_flag = None

    @staticmethod
    def to_dto(model):
        dto = NRankRecordInfoDto()
        dto.id = model.id
        dto.thumbnail_url = model.thumbnail_url
        dto.rank_detail_unit = model.rank_detail_unit
        dto.ad_rank_detail_unit = model.ad_rank_detail_unit
        dto.created_at = CustomUTCDateTime.convert_timezone_format(model.created_at)
        dto.nrank_record_id = model.nrank_record_id
        dto.deleted_flag = model.deleted_flag
        return dto
