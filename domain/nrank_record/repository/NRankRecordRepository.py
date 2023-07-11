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
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.workspace_id == id)
            ).scalars()
    
    def search_one_by_keyword_and_mall_name(self, keyword, mall_name):
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.keyword == keyword)
                .where(NRankRecordModel.mall_name == mall_name)
        ).first()