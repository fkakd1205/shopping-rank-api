from utils.db.v2.DBUtils import db_session
from sqlalchemy import select, text, update

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record_info.model.NRankRecordInfoModel import NRankRecordInfoModel
from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel

class NRankRecordRepository():
    def save(self, entity):
        db_session.add(entity)

    def search_list_by_workspace_id(self, workspace_id):
        query = select(NRankRecordModel).where(NRankRecordModel.workspace_id == workspace_id, NRankRecordModel.deleted_flag == False)
        return db_session.execute(query).scalars().all()
    
    def search_one_by_keyword_and_mall_name(self, keyword, mall_name):
        query = select(NRankRecordModel).where(NRankRecordModel.keyword == keyword).where(NRankRecordModel.mall_name == mall_name, NRankRecordModel.deleted_flag == False)
        return db_session.execute(query).scalar()
    
    def search_one(self, id):
        query = select(NRankRecordModel).where(NRankRecordModel.id == id)
        return db_session.execute(query).scalar()
    
    def deleted_one_related_nrank_record_info_and_nrank_recrod_detail(self, id):
        query = text("""
            UPDATE nrank_record record
            LEFT OUTER JOIN nrank_record_info info ON info.nrank_record_id = record.id
            LEFT OUTER JOIN nrank_record_detail detail ON detail.nrank_record_info_id = info.id
            SET record.deleted_flag = True, info.deleted_flag = True, detail.deleted_flag = True
            WHERE record.id = :id
        """
        )
        params = {"id" : id}
        db_session.execute(query, params)
