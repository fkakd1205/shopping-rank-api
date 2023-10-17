from sqlalchemy import select, text

from domain.nrank_record_info.model.NRankRecordInfoModel import NRankRecordInfoModel

from utils import get_db_session
from enums.NRankRecordInfoStatusEnum import NRankRecordInfoStatusEnum

NRANK_INFO_MAX_SEARCH_UNIT = 20

class NRankRecordInfoRepository():

    def save(self, model):
        get_db_session().add(model)

    def search_one(self, id):
        query = select(NRankRecordInfoModel)\
            .where(NRankRecordInfoModel.id == id)
        
        return get_db_session().execute(query).scalar()

    def search_list_by_record_ids(self, record_ids):
        query = select(NRankRecordInfoModel)\
            .where(
                NRankRecordInfoModel.nrank_record_id.in_(record_ids),
                NRankRecordInfoModel.deleted_flag == False,
                NRankRecordInfoModel.status != NRankRecordInfoStatusEnum.FAIL.value
            )
        
        return get_db_session().execute(query).scalars().all()
    
    def search_latest_list_by_record_id(self, record_id):
        query = select(NRankRecordInfoModel)\
            .where(
                NRankRecordInfoModel.nrank_record_id == record_id,
                NRankRecordInfoModel.deleted_flag == False,
                NRankRecordInfoModel.status != NRankRecordInfoStatusEnum.FAIL.value
            )\
            .order_by(NRankRecordInfoModel.created_at.desc())\
            .limit(NRANK_INFO_MAX_SEARCH_UNIT)
        
        return get_db_session().execute(query).scalars().all()

    # deprecated
    def search_latest_list_by_record_ids(self, record_ids):
        """nrank record별 최근 생성된 nrank record info를 특정 개수만큼 조회한다"""
    
        query = text("""
            SELECT *
            FROM (
                SELECT *, RANK() OVER (PARTITION BY info.nrank_record_id ORDER BY info.created_at DESC) AS search_order
                FROM nrank_record_info info
                WHERE info.nrank_record_id in :record_ids
                     AND info.deleted_flag = false
                     AND info.status != 'FAIL'
            ) as result
            WHERE result.search_order <= :max_search_unit
            ORDER BY result.created_at ASC
        """
        )
        params = {
            "record_ids": record_ids,
            "max_search_unit": NRANK_INFO_MAX_SEARCH_UNIT
        }

        return get_db_session().execute(query, params)
    
    # 삭제된 것도 포함해야 함
    def search_count_by_period_and_workspace_id(self, start_date, end_date, workspace_id):
        query = text("""
            SELECT COUNT(info.id)
            FROM nrank_record_info info
            JOIN nrank_record record ON record.id = info.nrank_record_id
            WHERE record.workspace_id = :workspace_id AND info.status != :status AND info.created_at BETWEEN :start_date AND :end_date
        """
        )
        params = {
            "workspace_id": workspace_id,
            "status": NRankRecordInfoStatusEnum.FAIL.value,
            "start_date": start_date,
            "end_date": end_date
        }

        return get_db_session().execute(query, params).scalar()
    
    def search_list_by_status(self, status):
        query = select(NRankRecordInfoModel)\
            .where(NRankRecordInfoModel.status == status.value)
        
        return get_db_session().execute(query).scalars().all()
    
    def search_list_by_ids(self, ids):
        query = select(NRankRecordInfoModel)\
            .where(NRankRecordInfoModel.id.in_(ids))
        
        return get_db_session().execute(query).scalars().all()