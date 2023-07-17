from utils.db.DBUtils import db

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from utils.date.DateTimeUtils import DateTimeUtils

class NRankRecordRepository():
    def save(self, entity):
        try:
            db.session.add(entity)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def search_list_by_workspace_id(self, id):
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.workspace_id == id)
        ).scalars().all()
    
    def search_one_by_keyword_and_mall_name(self, keyword, mall_name):
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.keyword == keyword)
                .where(NRankRecordModel.mall_name == mall_name)
        ).scalar()
    
    def search_one(self, id):
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.id == id)
        ).scalar()
    
    def delete_one(self, entity):
        try:
            db.session.delete(entity)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def change_last_searched_at(self, entity):
        try:
            entity.last_searched_at = DateTimeUtils.get_current_datetime()
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        
