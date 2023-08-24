import time
import uuid
from sqlalchemy import select

from domain.nrank_record.dto.NRankRecordDto import NRankRecordDto
from domain.nrank_record.model.NRankRecordModel import NRankRecordModel
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository

from utils import DateTimeUtils, CustomCookieUtils, db_session
from exception.types.CustomException import *
from enums.NRankRecordStatusEnum import NRankRecordStatusEnum

from decorators import *
from exception.types.CustomException import *

class TestService():
    
    # @celery.task
    def celery_test():
        print("celery_test start!!")
        time.sleep(5)
        print("celery_test finish!!")

    @transactional
    def test(self):
        print(DateTimeUtils.get_current_datetime())
        print(CustomCookieUtils.ACCESS_TOKEN_COOKIE_EXPIRATION)
        nrank_record_repository = NRankRecordRepository()
        dto = NRankRecordDto()

        workspace_id = "effd1e52-6b7f-4d13-92e2-a5b35a8b5373"
        user_id = "212935ba-a222-40a6-8827-dcafedd3cd6c"

        dto.id = uuid.uuid4()
        dto.keyword = 'test test'
        dto.mall_name = 'test test'
        dto.status = NRankRecordStatusEnum.NONE.value
        dto.status_updated_at = None
        dto.workspace_id = workspace_id
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = user_id
        dto.current_nrank_record_info_id = None
        dto.deleted_flag = False

        # keyword & mall_name 중복검사
        # self.check_duplication(dto)
        time.sleep(4)

        # new_model = NRankRecordModel.to_model(dto)
        # nrank_record_repository.save(new_model)
        results = nrank_record_repository.search_list_by_workspace_id(workspace_id)

        # raise CustomDuplicationException("test hihi")

    @transactional
    def test2(self):
        query = select(NRankRecordModel).where(NRankRecordModel.workspace_id == "effd1e52-6b7f-4d13-92e2-a5b35a8b5373", NRankRecordModel.deleted_flag == False)
        db = db_session()
        db.execute(query).scalars().all()
        db.close()

# @transactional
# def test(self):
#     nrank_record_repository = NRankRecordRepository()
#     dto = NRankRecordDto()
    
#     workspace_id = "effd1e52-6b7f-4d13-92e2-a5b35a8b5373"
#     user_id = "212935ba-a222-40a6-8827-dcafedd3cd6c"
    
#     dto.id = uuid.uuid4()
#     dto.keyword = 'test test'
#     dto.mall_name = 'test test'
#     dto.status = NRankRecordStatusEnum.NONE.value
#     dto.status_updated_at = None
#     dto.workspace_id = workspace_id
#     dto.created_at = DateTimeUtils.get_current_datetime()
#     dto.created_by_member_id = user_id
#     dto.current_nrank_record_info_id = None
#     dto.deleted_flag = False

#     # keyword & mall_name 중복검사
#     # self.check_duplication(dto)
#     time.sleep(3)
    
    # new_model = NRankRecordModel.to_model(dto)
    # nrank_record_repository.save(new_model)

