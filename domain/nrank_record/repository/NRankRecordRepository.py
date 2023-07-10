from utils.db.DBUtils import db

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel

class NRankRecordRepository():
    def save(self, data):
        db.session.add(data)
        db.session.commit()

    def search_list_by_workspace_id(self, id):
        return db.session.query(NRankRecordModel).filter(NRankRecordModel.workspace_id == id).all()
    
    def search_one(self, id):
        return db.session.query(NRankRecordModel).filter(NRankRecordModel.id == id).one()