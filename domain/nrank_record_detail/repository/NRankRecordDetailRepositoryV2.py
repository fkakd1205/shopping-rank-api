from utils.db.v2.DBUtils import db_session
from sqlalchemy import select, delete

from domain.nrank_record_detail.model.NRankRecordDetailModelV2 import NRankRecordDetailModel

class NRankRecordDetailRepository():

    def bulk_save(self, entities):
        try:
            # 객체 리스트를 대량 저장
            # bulk_insert_mappings()는 dict list를 대량 저장
            # add_all()은 반복적으로 add()를 실행
            db_session.bulk_save_objects(entities)
            db_session.commit()
        except:
            db_session.rollback()
        finally:
            db_session.close()

    def search_list_by_record_info_id(self, record_info_id):
        query = select(NRankRecordDetailModel).where(NRankRecordDetailModel.nrank_record_info_id == record_info_id)
        
        return db_session.execute(query).scalars().all()
    
    def bulk_delete_by_record_info_ids(self, record_info_ids):
        try:
            query = delete(NRankRecordDetailModel).where(NRankRecordDetailModel.nrank_record_info_id.in_(record_info_ids))
            db_session.execute(query)
            db_session.commit()
        except:
            db_session.rollback()
        finally:
            db_session.close()
        