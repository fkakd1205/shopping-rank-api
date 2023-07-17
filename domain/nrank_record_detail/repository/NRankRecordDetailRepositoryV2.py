from utils.db.DBUtils import db

from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel

class NRankRecordDetailRepository():

    def bulk_save(self, entities):
        try:
            db.session.bulk_save_objects(entities)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def search_list_by_record_id(self, record_id):
        return db.session.execute(
            db
                .select(NRankRecordDetailModel)
                .where(NRankRecordDetailModel.nrank_record_id == record_id)
        ).scalars().all()

    def bulk_delete(self, record_id):
        try:
            db.session.execute(
                db
                    .delete(NRankRecordDetailModel)
                    .where(NRankRecordDetailModel.nrank_record_id == record_id)
            )
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        