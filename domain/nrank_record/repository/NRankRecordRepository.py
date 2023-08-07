from utils.db.v2.DBUtils import db_session
from sqlalchemy import select, text

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel

class NRankRecordRepository():
    def save(self, entity):
        db_session.add(entity)

    def search_list_by_workspace_id(self, workspace_id):
        query = select(NRankRecordModel).where(NRankRecordModel.workspace_id == workspace_id, NRankRecordModel.deleted_flag == False)
        return db_session.execute(query).scalars().all()
    
    def search_list_by_ids_and_workspace_id(self, ids, workspace_id):
        query = select(NRankRecordModel).where(NRankRecordModel.workspace_id == workspace_id, NRankRecordModel.id.in_(ids))
        return db_session.execute(query).scalars().all()

    def search_one_by_keyword_and_mall_name(self, keyword, mall_name, workspace_id):
        query = select(NRankRecordModel).where(NRankRecordModel.keyword == keyword).where(NRankRecordModel.mall_name == mall_name, NRankRecordModel.deleted_flag == False, NRankRecordModel.workspace_id == workspace_id)
        return db_session.execute(query).scalar()
    
    def search_one(self, id):
        query = select(NRankRecordModel).where(NRankRecordModel.id == id)
        return db_session.execute(query).scalar()
    
    def soft_delete_one_and_related_all(self, id):
        """soft delete one and related nrank record infos and nrank record details
        
        Keyword arguments:
        id -- nrank record id
        """
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
