from utils.db.DBUtils import db

from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel

class NRankRecordDetailOfNRankRecordRepository():
    
    def bulk_delete(self, record_id):
        try:
            NRankRecordDetailModel.query.filter(NRankRecordDetailModel.nrank_record_id == record_id).delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()