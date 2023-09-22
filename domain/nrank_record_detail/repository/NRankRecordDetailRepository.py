from utils import get_db_session
from sqlalchemy import select

from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel

class NRankRecordDetailRepository():

    def bulk_save(self, entities):
        get_db_session().bulk_save_objects(entities)

    def search_list_by_record_info_id(self, record_info_id):
        query = select(NRankRecordDetailModel)\
            .where(NRankRecordDetailModel.nrank_record_info_id == record_info_id)
        
        return get_db_session().execute(query).scalars().all()
        