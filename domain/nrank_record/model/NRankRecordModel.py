from utils.db.DBUtils import db
from utils.type.CustomUTCDateTime import CustomUTCDateTime

class NRankRecordModel(db.Model):
    __tablename__ = 'nrank_record'

    cid = db.Column("cid", db.BigInteger, primary_key=True, autoincrement=True)
    id = db.Column("id", db.String(36), unique=True, nullable=False)
    keyword = db.Column("keyword", db.String(50), nullable=False)
    mall_name = db.Column("mall_name", db.String(50), nullable=False)
    workspace_id = db.Column("workspace_id", db.String(36), nullable=False)
    # last_searched_at = db.Column("last_searched_at", CustomUTCDateTime, nullable=False)
    created_at = db.Column("created_at", CustomUTCDateTime, nullable=False)
    created_by_member_id = db.Column("created_by_member_id", db.String(36), nullable=False)

    def __init__(self):
        self.id = None
        self.keyword = None
        self.mall_name = None
        self.workspace_id = None
        self.created_at = None
        self.created_by_member_id = None

    @staticmethod
    def to_entity(dto):
        entity = NRankRecordModel()
        entity.id = dto.id
        entity.keyword = dto.keyword
        entity.mall_name = dto.mall_name
        entity.workspace_id = dto.workspace_id
        entity.created_at = dto.created_at
        entity.created_by_member_id = dto.created_by_member_id
        return entity
