from utils import db_session
from sqlalchemy import select, func

from domain.nrank_record.model.NRankRecordModel import NRankRecordModel

from enums.PageSortDirectionEnum import PageSortDirectionEnum
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

from exception.types.CustomException import *

class NRankRecordRepositoryV2():

    def search_list_by_workspace_id_by_page(self, workspace_id, filter, pageable):
        query = select(NRankRecordModel)\
            .where(
                NRankRecordModel.workspace_id == workspace_id,
                NRankRecordModel.deleted_flag == False
            )
        
        query = self.set_query_by_condition(filter, query)
        query = self.eq_category(filter, query)
        query = self.eq_status(filter, query)
        query = self.eq_page(pageable, query)

        return db_session.execute(query).scalars().all()
    
    def search_list_count_by_workspace_id(self, workspace_id, filter) -> (int):
        query = select(func.count())\
            .where(
                NRankRecordModel.workspace_id == workspace_id,
                NRankRecordModel.deleted_flag == False
            )
        
        query = self.set_query_by_condition(filter, query)
        query = self.eq_category(filter, query)
        query = self.eq_status(filter, query)

        return db_session.execute(query).scalar()
    
    def set_query_by_condition(self, filter, query):
        """search condition & search query(검색 필드 및 입력갑) 검색
        
        filter
        - search_condition : 검색 조건 필드
        - search_query : 검색 조건 입력값
        """
        if(filter.search_condition is None or filter.search_query is None):
            return query
        
        if(getattr(NRankRecordModel, filter.search_condition) is None):
            return query
        
        return query.where(getattr(NRankRecordModel, filter.search_condition).like(f"%{filter.search_query}%"))

    def eq_category(self, filter, query):
        """search category(카테고리) 검색
        
        filter
        - search_category_id : 검색 카테고리 id
        """
        if(filter.search_category_id is None):
            return query
    
        return query.where(NRankRecordModel.nrank_record_category_id == filter.search_category_id)
    
    def eq_status(self, filter, query):
        """search status(랭킹 내역 상태) 검색
        
        filter
        - search_status : 랭킹 내역 상태
        """
        if(filter.search_status is None):
            return query

        return query.where(NRankRecordModel.status == NRankRecordStatusEnum(filter.search_status).value)
    
    def eq_page(self, pageable, query):
        """search page(페이지 조건) 검색
        
        pageable
        - offset : (pageable.page - 1) * pageable.size
        - size : 조회 사이즈
        """
        order_by_condition = self.get_order_by_condition(pageable)

        if(pageable.page < 0 or pageable.size < 0):
            return query

        query = query.order_by(order_by_condition)\
            .offset(((pageable.page - 1) * pageable.size))\
            .limit(pageable.size)
        
        return query
    
    def get_order_by_condition(self, pageable):
        """order_by_condition(정렬 조건) 설정
        
        pageable
        - sort_column : 정렬 항목
        - sort_direction : 정렬 방향
        """
        if(pageable.sort_column is None or pageable.sort_direction is None):
            return NRankRecordModel.created_at.desc()
        
        # NRankRecordModel에 sort_column이 존재하지 않을 경우 예외 처리
        try:
            sort_column = getattr(NRankRecordModel, pageable.sort_column)
        except:
            raise CustomInvalidValueException("올바른 요청이 아닙니다.")

        if(pageable.sort_direction == PageSortDirectionEnum.DESC):
            return sort_column.desc()
        elif(pageable.sort_direction == PageSortDirectionEnum.ASC):
            return sort_column.asc()
