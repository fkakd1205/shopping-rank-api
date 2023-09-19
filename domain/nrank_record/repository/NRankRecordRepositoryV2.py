from utils import db_session
from sqlalchemy import select

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel

from enums.PageSortDirectionEnum import PageSortDirectionEnum
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

class NRankRecordRepositoryV2():

    def search_list_by_workspace_id_by_page(self, workspace_id, filter, pageable):
        query = select(NRankRecordModel).where(NRankRecordModel.workspace_id == workspace_id, NRankRecordModel.deleted_flag == False)
        
        query = self.search_query_by_condition(filter, query)
        query = self.search_category(filter, query)
        query = self.search_status(filter, query)
        query = self.search_page(pageable, query)

        return db_session.execute(query).scalars().all()
    
    # TODO :: count만 결과로 가져오기
    def search_list_count_by_workspace_id(self, workspace_id, filter):
        query = select(NRankRecordModel).where(NRankRecordModel.workspace_id == workspace_id, NRankRecordModel.deleted_flag == False)
        
        query = self.search_query_by_condition(filter, query)
        query = self.search_category(filter, query)
        query = self.search_status(filter, query)

        return db_session.execute(query).scalars().all()
    
    def search_query_by_condition(self, filter, query):
        if(filter.search_condition is None or filter.search_query is None):
            return query
        
        if(getattr(NRankRecordModel, filter.search_condition) is None):
            return query
        
        return query.where(getattr(NRankRecordModel, filter.search_condition).like(f"%{filter.search_query}%"))

    def search_category(self, filter, query):
        if(filter.search_category_id is None):
            return query
    
        return query.where(NRankRecordModel.nrank_record_category_id == filter.search_category_id)
    
    def search_status(self, filter, query):
        if(filter.search_status is None):
            return query

        return query.where(NRankRecordModel.status == NRankRecordStatusEnum(filter.search_status).value)
    
    def search_page(self, pageable, query):
        order_by_condition = self.get_order_by_condition(pageable)

        query = query.order_by(order_by_condition)\
            .offset(pageable.offset)\
            .limit(pageable.size)
        
        return query
    
    def get_order_by_condition(self, pageable):
        if(pageable.sort_column is None or pageable.sort_direction is None):
            return NRankRecordModel.created_at.desc()
        
        sort_column = getattr(NRankRecordModel, pageable.sort_column, None)
        if(sort_column is None):
            return NRankRecordModel.created_at.desc()
        
        # offset setting
        pageable.offset = ((pageable.page - 1) * pageable.size)

        if(pageable.sort_direction == PageSortDirectionEnum.DESC):
            return sort_column.desc()
        elif(pageable.sort_direction == PageSortDirectionEnum.ASC):
            return sort_column.asc()
