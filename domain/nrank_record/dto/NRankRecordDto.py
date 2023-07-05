class NRankRecordDto():
    def __init__(self):
        self.id = None
        self.keyword = None
        self.mall_name = None
        self.workspace_id = None
        self.created_at = None
        self.created_by_member_id = None

    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id

    def get_keyword(self):
        return self.keyword
    
    def set_keyword(self, keyword):
        self.keyword = keyword

    def get_mall_name(self):
        return self.mall_name
    
    def set_mall_name(self, mall_name):
        self.mall_name = mall_name

    def get_workspace_id(self):
        return self.workspace_id
    
    def set_workspace_id(self, workspace_id):
        self.workspace_id = workspace_id

    def get_created_at(self):
        return self.created_at
    
    def set_created_at(self, created_at):
        self.created_at = created_at

    def get_created_by_member_id(self):
        return self.created_by_member_id

    def set_created_by_member_id(self, created_by_member_id):
        self.created_by_member_id = created_by_member_id

    @staticmethod
    def to_dto(entity):
        dto = NRankRecordDto()
        dto.set_id(entity.id)
        dto.set_keyword(entity.keyword)
        dto.set_mall_name(entity.mall_name)
        dto.set_workspace_id(entity.workspace_id)
        dto.set_created_at((entity.created_at).strftime("%Y-%m-%dT%H:%M:%SZ"))
        dto.set_created_by_member_id(entity.created_by_member_id)
        return dto.__dict__
