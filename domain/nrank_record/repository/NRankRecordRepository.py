from utils.db.v1.DBUtils import db
from sqlalchemy import select

from domain.nrank_record.model.NRankRecordModelV2 import NRankRecordModel

class NRankRecordRepository():
    def save(self, entity):
        try:
            db.session.add(entity)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def search_list_by_workspace_id(self, workspace_id):
        query = db.select(NRankRecordModel).where(NRankRecordModel.workspace_id == workspace_id)
        
        return db.execute(query).scalars().all()
    
    def search_one_by_keyword_and_mall_name(self, keyword, mall_name):
        query = db\
                    .select(NRankRecordModel)\
                    .where(NRankRecordModel.keyword == keyword)\
                    .where(NRankRecordModel.mall_name == mall_name)
        
        return db.session.execute(query).scalar()
    
    def search_one(self, id):
        query = db\
                .select(NRankRecordModel)\
                .where(NRankRecordModel.id == id)
        
        return db.session.execute(query).scalar()
    
    def delete_one(self, entity):
        try:
            db.session.delete(entity)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
