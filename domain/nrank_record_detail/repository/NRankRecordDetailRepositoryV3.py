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

    def search_list_by_record_info_id(self, record_info_id):
        return db.session.execute(
            db
                .select(NRankRecordDetailModel)
                .where(NRankRecordDetailModel.nrank_record_info_id == record_info_id)
        ).scalars().all()
        