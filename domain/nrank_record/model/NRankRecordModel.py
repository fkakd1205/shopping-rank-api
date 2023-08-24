from utils import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean

from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

class NRankRecordModel(Base):
    __tablename__ = 'nrank_record'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    keyword = Column("keyword", String(50), nullable=False)
    status = Column("status", String(10), nullable=False)
    status_updated_at = Column("status_updated_at", DateTime(timezone=True), nullable=True)
    mall_name = Column("mall_name", String(50), nullable=False)
    workspace_id = Column("workspace_id", String(36), nullable=False)
    created_at = Column("created_at", DateTime(timezone = True), nullable=True)
    created_by_member_id = Column("created_by_member_id", String(36), nullable=False)
    current_nrank_record_info_id = Column("current_nrank_record_info_id", String(36), nullable=False)
    deleted_flag = Column("deleted_flag", Boolean, nullable=False)

    def __init__(self):
        self.id = None
        self.keyword = None
        self.mall_name = None
        self.status = NRankRecordStatusEnum.NONE.value
        self.status_updated_at = None
        self.workspace_id = None
        self.created_at = None
        self.created_by_member_id = None
        self.current_nrank_record_info_id = None
        self.deleted_flag = False

    @staticmethod
    def to_model(dto):
        model = NRankRecordModel()
        model.id = dto.id
        model.keyword = dto.keyword
        model.mall_name = dto.mall_name
        model.status = dto.status
        model.status_updated_at = None
        model.workspace_id = dto.workspace_id
        model.created_at = dto.created_at
        model.created_by_member_id = dto.created_by_member_id
        model.current_nrank_record_info_id = dto.current_nrank_record_info_id
        model.deleted_flag = dto.deleted_flag
        return model
