from utils.db.DBUtils import db

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel

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
        return NRankRecordModel.query.filter(NRankRecordModel.workspace_id == id).all()
    
    def search_one_by_keyword_and_mall_name(self, keyword, mall_name):
        return NRankRecordModel.query.filter(NRankRecordModel.keyword == keyword, NRankRecordModel.mall_name == mall_name).first()
    
    def search_one(self, id):
        return NRankRecordModel.query.filter(NRankRecordModel.id == id).one()
    
    def delete_one(self, entity):
        try:
            db.session.delete(entity)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        
