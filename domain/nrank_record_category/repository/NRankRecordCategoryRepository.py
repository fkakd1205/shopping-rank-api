from sqlalchemy import select, update

from domain.nrank_record_category.model.NRankRecordCategoryModel import NRankRecordCategoryModel

from utils import db_session

class NRankRecordCategoryRepository():
    
    def save(self, model):
        db_session.add(model)

    def search_one(self, id):
        query = select(NRankRecordCategoryModel).where(NRankRecordCategoryModel.id == id)
        return db_session.execute(query).scalar()

    def search_list_by_workspace_id(self, workspace_id):
        query = select(NRankRecordCategoryModel).where(NRankRecordCategoryModel.workspace_id == workspace_id, NRankRecordCategoryModel.deleted_flag == False)
        return db_session.execute(query).scalars().all()
    
    def search_one_by_name(self, name, workspace_id):
        query = select(NRankRecordCategoryModel).where(NRankRecordCategoryModel.name == name, NRankRecordCategoryModel.deleted_flag == False, NRankRecordCategoryModel.workspace_id == workspace_id)
        return db_session.execute(query).scalar()
    
    def soft_delete_one(self, id):
        query = update(NRankRecordCategoryModel).where(NRankRecordCategoryModel.id == id).values(deleted_flag = True)
        return db_session.execute(query)