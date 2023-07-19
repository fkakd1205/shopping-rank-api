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

    # class RelatedNRankRecordInfo():
    #     def __init__(self):
    #         self.id = None
    #         self.keyword = None
    #         self.mall_name = None
    #         self.workspace_id = None
    #         self.created_at = None
    #         self.created_by_member_id = None
    #         self.current_nrank_record_info_id = None

    #         self.infos = []

    #     @staticmethod
    #     def to_dto(model):
    #         dto = NRankRecordDto.RelatedNRankRecordInfo()
    #         print(model)

            # nrank_record = model.NRankRecordModel
            # nrank_record_infos = []
            # if(model.NRankRecordInfoModel is not None):
            #     nrank_record_infos.append(model.NRankRecordInfoModel)

            # dto.id = nrank_record.id
            # dto.keyword = nrank_record.keyword
            # dto.mall_name = nrank_record.mall_name
            # dto.workspace_id = nrank_record.workspace_id
            # dto.created_at = CustomUTCDateTime.convert_timezone_format(nrank_record.created_at)
            # dto.created_by_member_id = nrank_record.created_by_member_id
            # dto.current_nrank_record_info_id = nrank_record.current_nrank_record_info_id

            # dto.infos = list(map(lambda info_model: NRankRecordInfoDto.to_dto(info_model), nrank_record_infos))
            # return dto.__dict__

