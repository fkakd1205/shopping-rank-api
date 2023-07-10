from utils.db.DBUtils import db

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from utils.date.DateTimeUtils import DateTimeUtils

class NRankRecordOfNRankRecordDetailRepository():

    def search_one(self, id):
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.id == id)
        ).scalar()
    
    def change_last_searched_at(self, entity):
        try:
            entity.last_searched_at = DateTimeUtils.get_current_datetime()
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()