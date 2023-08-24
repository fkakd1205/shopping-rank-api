from utils import db_session
from sqlalchemy import select, text

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
    
    # 삭제된 것도 포함해야 함
    def search_count_by_period_and_workspace_id(self, start_date, end_date, workspace_id):
        query = text("""
            SELECT COUNT(info.id)
            FROM nrank_record_info info
            JOIN nrank_record record ON record.id = info.nrank_record_id
            WHERE record.workspace_id = :workspace_id AND info.created_at BETWEEN :start_date AND :end_date
        """
        )
        params = {"workspace_id": workspace_id, "start_date": start_date, "end_date": end_date}
        return db_session.execute(query, params).scalar()
    