from utils.type.CustomUTCDateTime import CustomUTCDateTime

class NRankRecordDto():
    def __init__(self):
        self.id = None
        self.keyword = None
        self.mall_name = None
        self.workspace_id = None
        self.last_searched_at = None
        self.created_at = None
        self.created_by_member_id = None

    @staticmethod
    def to_dto(entity):
        dto = NRankRecordDto()
        dto.id = entity.id
        dto.keyword = entity.keyword
        dto.mall_name = entity.mall_name
        dto.workspace_id = entity.workspace_id
        dto.last_searched_at = CustomUTCDateTime.convert_timezone_format(entity.last_searched_at)
        dto.created_at = CustomUTCDateTime.convert_timezone_format(entity.created_at)
        dto.created_by_member_id = entity.created_by_member_id
        return dto.__dict__
