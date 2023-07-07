from utils.db.DBUtils import db

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel

class NRankRecordRepository():
    def save(self, data):
        db.session.add(data)
        db.session.commit()

    def search_list_by_member_id(self, member_id):
        return db.session.query(NRankRecordModel).filter(NRankRecordModel.created_by_member_id == str(member_id)).all()
    
    def search_one(self, id):
        return db.session.query(NRankRecordModel).filter(NRankRecordModel.id == id).one()