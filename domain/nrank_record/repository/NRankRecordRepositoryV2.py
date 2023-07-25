from utils.db.v2.DBUtils import db_session
from sqlalchemy import select

from domain.nrank_record.model.NRankRecordModelV2 import NRankRecordModel

class NRankRecordRepository():
    def save(self, entity):
        try:
            db_session.add(entity)
            db_session.commit()
        except:
            db_session.rollback()
        finally:
            db_session.close()

    def search_list_by_workspace_id(self, workspace_id):
        query = select(NRankRecordModel).where(NRankRecordModel.workspace_id == workspace_id)
        return db_session.execute(query).scalars().all()
    
    def search_one_by_keyword_and_mall_name(self, keyword, mall_name):
        query = select(NRankRecordModel).where(NRankRecordModel.keyword == keyword).where(NRankRecordModel.mall_name == mall_name)
        return db_session.execute(query).scalar()
    
    def search_one(self, id):
        query = select(NRankRecordModel).where(NRankRecordModel.id == id)
        return db_session.execute(query).scalar()
    
    def delete_one(self, entity):
        try:
            db_session.delete(entity)
            db_session.commit()
        except:
            db_session.rollback()
        finally:
            db_session.close()
