from utils.type.CustomUTCDateTime import CustomUTCDateTime

class NRankRecordDto():
    def __init__(self):
        self.id = None
        self.keyword = None
        self.mall_name = None
        self.workspace_id = None
        self.created_at = None
        self.created_by_member_id = None
        self.current_nrank_record_info_id = None

    @staticmethod
    def to_dto(model):
        dto = NRankRecordDto()
        dto.id = model.id
        dto.keyword = model.keyword
        dto.mall_name = model.mall_name
        dto.workspace_id = model.workspace_id
        dto.created_at = CustomUTCDateTime.convert_timezone_format(model.created_at)
        dto.created_by_member_id = model.created_by_member_id
        dto.current_nrank_record_info_id = model.current_nrank_record_info_id
        return dto.__dict__
