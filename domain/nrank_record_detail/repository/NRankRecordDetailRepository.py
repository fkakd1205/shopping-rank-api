from utils.db.DBUtils import db

from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel

class NRankRecordDetailRepository():

    def bulk_save(self, entities):
        try:
            db.session.bulk_save_objects(entities)
            db.session.commit()
        except:
            db.session.rollback()
            raise
            # TODO :: 예외를 발생시키고, service단에서 nrank_record의 last_searched_at의 업데이트를 막아햐함
        finally:
            db.session.close()

    def search_list_by_record_id(self, record_id):
        return db.session.execute(
            db
                .select(NRankRecordDetailModel)
                .where(NRankRecordDetailModel.nrank_record_id == record_id)
            ).scalars()
            # ).scalars().all()
        