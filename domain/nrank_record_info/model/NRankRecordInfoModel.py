from utils import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, Integer

class NRankRecordInfoModel(Base):
    __tablename__ = 'nrank_record_info'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    thumbnail_url = Column("thumbnail_url", String(600), nullable=True)
    rank_detail_unit = Column("rank_detail_unit", Integer, nullable=True)
    ad_rank_detail_unit = Column("ad_rank_detail_unit", Integer, nullable=True)
    created_at = Column("created_at", DateTime(timezone = True), nullable=True)
    nrank_record_id = Column("nrank_record_id", String(36), nullable=False)
    deleted_flag = Column("deleted_flag", Boolean, nullable=False)

    def __init__(self):
        self.id = None
        self.thumbnail_url = None
        self.rank_detail_unit = None
        self.ad_rank_detail_unit = None
        self.created_at = None
        self.nrank_record_id = None
        self.deleted_flag = False

    @staticmethod
    def to_model(dto):
        model = NRankRecordInfoModel()
        model.id = dto.id
        model.thumbnail_url = dto.thumbnail_url
        model.rank_detail_unit = dto.rank_detail_unit
        model.ad_rank_detail_unit = dto.ad_rank_detail_unit
        model.created_at = dto.created_at
        model.nrank_record_id = dto.nrank_record_id
        model.deleted_flag = dto.deleted_flag
        return model
