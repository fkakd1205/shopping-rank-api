from utils.db.v1.DBUtils import db

from domain.nrank_record_info.model.NRankRecordInfoModelV2 import NRankRecordInfoModel

class NRankRecordInfoRepository():

    def save(self, entity):
        try:
            db.session.add(entity)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        
    def bulk_delete(self, record_id):
        try:
            query = db\
                    .delete(NRankRecordInfoModel)\
                    .where(NRankRecordInfoModel.nrank_record_id == record_id)
            
            db.sesison.execute(query)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def searh_list_by_record_ids(self, record_ids):
        query = db.select(NRankRecordInfoModel).where(NRankRecordInfoModel.nrank_record_id.in_(record_ids))
        return db.execute(query).scalars().all()
    