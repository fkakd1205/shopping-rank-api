from utils.db.DBUtils import db

class NRankRecordModel(db.Model):
    __tablename__ = 'nrank_record'

    cid = db.Column("cid", db.BigInteger, primary_key=True, autoincrement=True)
    id = db.Column("id", db.String(36), unique=True, nullable=False)
    keyword = db.Column("keyword", db.String(50), nullable=False)
    mall_name = db.Column("mall_name", db.String(50), nullable=False)
    workspace_id = db.Column("workspace_id", db.String(36), nullable=False)
    created_at = db.Column("created_at", db.DateTime(timezone=True), nullable=False)
    created_by_member_id = db.Column("created_by_member_id", db.String(36), nullable=False)

    def __init__(self):
        self.id = None
        self.keyword = None
        self.mall_name = None
        self.workspace_id = None
        self.created_at = None
        self.created_by_member_id = None

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
    def to_entity(dto):
        entity = NRankRecordModel()
        entity.set_id(dto.id)
        entity.set_keyword(dto.keyword)
        entity.set_mall_name(dto.mall_name)
        entity.set_workspace_id(dto.workspace_id)
        entity.set_created_at((dto.created_at).strftime("%Y-%m-%d %H:%M:%S"))
        entity.set_created_by_member_id(dto.created_by_member_id)
        return entity
