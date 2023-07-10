from utils.db.DBUtils import db

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel

class NRankRecordRepository():
    def save(self, entity):
        db.session.add(entity)
        db.session.commit()

    def search_list_by_workspace_id(self, id):
        return db.session.execute(
            db
                .select(NRankRecordModel)
                .where(NRankRecordModel.workspace_id == id)
            ).scalars()