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

    def search_list_by_workspace_id(self, workspace_id):
        # v2
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.workspace_id == workspace_id)
        ).scalars().all()

        # v1
        # return db.session.execute(
        #     db
        #         .select(NRankRecordModel, NRankRecordInfoModel)
        #         .join(NRankRecordInfoModel, 
        #               NRankRecordModel.id == NRankRecordInfoModel.nrank_record_id,
        #               isouter=True)
        #         .where(NRankRecordModel.workspace_id == workspace_id)
        # ).fetchall()
    
        # v3
        # return db.session.query(NRankRecordModel, NRankRecordInfoModel)\
        #     .outerjoin(NRankRecordInfoModel, NRankRecordModel.id == NRankRecordInfoModel.nrank_record_id)\
        #     .filter(NRankRecordModel.workspace_id == workspace_id)\
        #     .all()
    
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
