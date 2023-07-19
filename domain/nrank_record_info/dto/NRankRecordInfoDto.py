from utils.type.CustomUTCDateTime import CustomUTCDateTime

class NRankRecordInfoDto():
    def __init__(self):
        self.id = None
        self.thumbnail_url = None
        self.created_at = None
        self.nrank_record_id = None

    @staticmethod
    def to_dto(model):
        dto = NRankRecordInfoDto()
        dto.id = model.id
        dto.thumbnail_url = model.thumbnail_url
        dto.created_at = CustomUTCDateTime.convert_timezone_format(model.created_at)
        dto.nrank_record_id = model.nrank_record_id
        return dto.__dict__
