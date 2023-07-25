from utils.db.v2.DBUtils import db_session
from sqlalchemy import select, delete

from domain.nrank_record_info.model.NRankRecordInfoModelV2 import NRankRecordInfoModel

class NRankRecordInfoRepository():

    def save(self, entity):
        try:
            db_session.add(entity)
            db_session.commit()
        except:
            db_session.rollback()
        finally:
            db_session.close()
        
    def bulk_delete_by_ids(self, record_info_ids):
        try:
            query = delete(NRankRecordInfoModel).where(NRankRecordInfoModel.id.in_(record_info_ids))
            db_session.execute(query)
            db_session.commit()
        except:
            db_session.rollback()
        finally:
            db_session.close()

    def searh_list_by_record_ids(self, record_ids):
        query = select(NRankRecordInfoModel).where(NRankRecordInfoModel.nrank_record_id.in_(record_ids))
        return db_session.execute(query).scalars().all()
    
    def search_list_by_record_id(self, record_id):
        query = select(NRankRecordInfoModel).where(NRankRecordInfoModel.nrank_record_id == record_id)
        return db_session.execute(query).scalars().all()
    