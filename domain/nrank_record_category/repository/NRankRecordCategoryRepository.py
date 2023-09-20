from sqlalchemy import select, update, text

from domain.nrank_record_category.model.NRankRecordCategoryModel import NRankRecordCategoryModel

from utils import db_session

class NRankRecordCategoryRepository():
    
    def save(self, model):
        db_session.add(model)

    def search_one(self, id):
        query = select(NRankRecordCategoryModel)\
            .where(NRankRecordCategoryModel.id == id)
        
        return db_session.execute(query).scalar()

    def search_list_by_workspace_id(self, workspace_id):
        query = select(NRankRecordCategoryModel)\
            .where(
                NRankRecordCategoryModel.workspace_id == workspace_id,
                NRankRecordCategoryModel.deleted_flag == False
            )
        
        return db_session.execute(query).scalars().all()
    
    def search_one_by_name(self, name, workspace_id):
        query = select(NRankRecordCategoryModel)\
            .where(
                NRankRecordCategoryModel.name == name,
                NRankRecordCategoryModel.deleted_flag == False,
                NRankRecordCategoryModel.workspace_id == workspace_id
            )
        
        return db_session.execute(query).scalar()
    
    def soft_delete_one_and_related_all(self, id):
        """soft delete one and update related nrank record

        nrank_record_category의 deleted_flag를 True로 변경한다.
        nrank_record의 nrank_record_category_id를 Null로 변경한다.
        - id : nrank record category id
        """
        query = text("""
            UPDATE nrank_record_category category
            JOIN nrank_record record ON record.nrank_record_category_id = category.id
            SET category.deleted_flag = True, record.nrank_record_category_id = Null
            WHERE category.id = :id
        """)
        params = {"id": id}

        return db_session.execute(query, params)