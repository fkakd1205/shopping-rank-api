from utils.db.v2.DBUtils import Base
from sqlalchemy import Column, BigInteger, String, DateTime

class NRankRecordModel(Base):
    __tablename__ = 'nrank_record'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    keyword = Column("keyword", String(50), nullable=False)
    mall_name = Column("mall_name", String(50), nullable=False)
    workspace_id = Column("workspace_id", String(36), nullable=False)
    created_at = Column("created_at", DateTime(timezone = True), nullable=True)
    created_by_member_id = Column("created_by_member_id", String(36), nullable=False)
    current_nrank_record_info_id = Column("current_nrank_record_info_id", String(36), nullable=False)

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
