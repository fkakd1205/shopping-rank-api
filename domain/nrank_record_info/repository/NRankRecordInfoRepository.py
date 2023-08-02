from utils.db.v2.DBUtils import db_session
from sqlalchemy import select

from domain.nrank_record_info.model.NRankRecordInfoModel import NRankRecordInfoModel

class NRankRecordInfoRepository():

    def save(self, entity):
        db_session.add(entity)

    def search_one(self, id):
        query = select(NRankRecordInfoModel).where(NRankRecordInfoModel.id == id)
        return db_session.execute(query).scalar()

    def search_list_by_record_ids(self, record_ids):
        query = select(NRankRecordInfoModel).where(NRankRecordInfoModel.nrank_record_id.in_(record_ids))
        return db_session.execute(query).scalars().all()
    