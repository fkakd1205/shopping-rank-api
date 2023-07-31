from utils.type.CustomUTCDateTime import CustomUTCDateTime

class NRankRecordInfoDto():
    def __init__(self):
        self.id = None
        self.thumbnail_url = None
        self.rank_detail_unit = None
        self.ad_rank_detail_unit = None
        self.created_at = None
        self.nrank_record_id = None
        self.deleted_flag = None

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
