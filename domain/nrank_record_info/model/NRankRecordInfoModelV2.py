from utils.db.v2.DBUtils import Base
from sqlalchemy import Column, BigInteger, String, DateTime

class NRankRecordInfoModel(Base):
    __tablename__ = 'nrank_record_info'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    thumbnail_url = Column("thumbnail_url", String(600), nullable=True)
    created_at = Column("created_at", DateTime(timezone = True), nullable=True)
    nrank_record_id = Column("nrank_record_id", String(36), nullable=False)

    def __init__(self):
        self.id = None
        self.thumbnail_url = None
        self.created_at = None
        self.nrank_record_id = None

    @staticmethod
    def to_model(dto):
        model = NRankRecordInfoModel()
        model.id = dto.id
        model.thumbnail_url = dto.thumbnail_url
        model.created_at = dto.created_at
        model.nrank_record_id = dto.nrank_record_id
        return model
