from utils.db.DBUtils import db

class NRankRecordModel(db.Model):
    __tablename__ = 'nrank_record'

    cid = db.Column("cid", db.BigInteger, primary_key=True, autoincrement=True)
    id = db.Column("id", db.String(36), unique=True, nullable=False)
    keyword = db.Column("keyword", db.String(50), nullable=False)
    mall_name = db.Column("mall_name", db.String(50), nullable=False)
    workspace_id = db.Column("workspace_id", db.String(36), nullable=False)
    created_at = db.Column("created_at", db.DateTime(timezone = True), nullable=True)
    created_by_member_id = db.Column("created_by_member_id", db.String(36), nullable=False)
    current_nrank_record_info_id = db.Column("current_nrank_record_info_id", db.String(36), nullable=False)

    def __init__(self):
        self.id = None
        self.keyword = None
        self.mall_name = None
        self.workspace_id = None
        self.created_at = None
        self.created_by_member_id = None
        self.current_nrank_record_info_id = None

    @staticmethod
    def to_model(dto):
        model = NRankRecordModel()
        model.id = dto.id
        model.keyword = dto.keyword
        model.mall_name = dto.mall_name
        model.workspace_id = dto.workspace_id
        model.created_at = dto.created_at
        model.created_by_member_id = dto.created_by_member_id
        model.current_nrank_record_info_id = dto.current_nrank_record_info_id
        return model
