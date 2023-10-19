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
        
    # deprecated...
    # def search_list_by_record_info_ids_and_pid_and_iid(self, info_ids, mall_product_id, item_id):
    #     query = select(NRankRecordDetailModel)\
    #         .where(NRankRecordDetailModel.nrank_record_info_id.in_(info_ids),
    #             NRankRecordDetailModel.mall_product_id == mall_product_id,
    #             NRankRecordDetailModel.item_id == item_id,
    #             NRankRecordDetailModel.deleted_flag == False
    #         )
        
    #     return get_db_session().execute(query).scalars().all()
    
    def search_list_by_record_info_ids_and_mpids_and_iids(self, info_ids, mall_product_ids, item_ids):
        query = select(NRankRecordDetailModel)\
            .where(NRankRecordDetailModel.nrank_record_info_id.in_(info_ids),
                NRankRecordDetailModel.mall_product_id.in_(mall_product_ids),
                NRankRecordDetailModel.item_id.in_(item_ids),
                NRankRecordDetailModel.deleted_flag == False
            )
        
        return get_db_session().execute(query).scalars().all()
