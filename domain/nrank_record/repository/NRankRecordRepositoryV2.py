from utils.db.v2.DBUtils import db_session
from sqlalchemy import select, text, and_

from domain.nrank_record.model.NRankRecordModelV2 import NRankRecordModel
from domain.nrank_record_info.model.NRankRecordInfoModelV2 import NRankRecordInfoModel
from domain.nrank_record_detail.model.NRankRecordDetailModelV2 import NRankRecordDetailModel

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
    
    # deprecated
    # def delete_one_by_id(self, id):
    #     query = delete(NRankRecordModel).where(NRankRecordModel.id == id)
    #     return db_session.execute(query)
    
    def deleted_one_related_nrank_record_info_and_nrank_recrod_detail(self, id):
        query = text("""
            UPDATE nrank_record record, nrank_record_info info, nrank_record_detail detail
            SET record.deleted_flag = True, info.deleted_flag = True, detail.deleted_flag = True
            WHERE record.id = :id AND info.nrank_record_id = :id AND detail.nrank_record_info_id = info.id
        """
        )
        params = {"id" : id}
        db_session.execute(query, params)
        
