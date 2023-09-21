from utils import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, CheckConstraint


class NRankRecordCategoryModel(Base):
    __tablename__ = 'nrank_record_category'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    name = Column("name", String(20), nullable=False)
    created_at = Column("created_at", DateTime(timezone = True), nullable=True)
    updated_at = Column("updated_at", DateTime(timezone = True), nullable=True)
    created_by_member_id = Column("created_by_member_id", String(36), nullable=False)
    deleted_flag = Column("deleted_flag", Boolean, nullable=False)
    workspace_id = Column("workspace_id", String(36), nullable=False)

    def __init__(self):
        self.id = None
        self.name = None
        self.created_at = None
        self.updated_at = None
        self.created_by_member_id = None
        self.deleted_flag = False
        self.workspace_id = None

    @staticmethod
    def to_model(dto):
        model = NRankRecordCategoryModel()
        model.id = dto.id
        model.name = dto.name
        model.created_at = dto.created_at
        model.updated_at = dto.updated_at
        model.created_by_member_id = dto.created_by_member_id
        model.deleted_flag = dto.deleted_flag
        model.workspace_id = dto.workspace_id
        return model