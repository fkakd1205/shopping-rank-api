from domain.workspace.dto.WorkspaceNRankSearchInfoDto import WorkspaceNRankSearchInfoDto
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository

from utils import DateTimeUtils, MemberPermissionUtils
from exception.types.CustomException import *

class WorkspaceService():

    def check_nrank_search_allowed_count(self):
        memberUtils = MemberPermissionUtils()
        searched_cnt = self.get_nrank_searched_count()

        allowed_search_cnt = memberUtils.get_nrank_search_allowed_count()
        if(searched_cnt >= allowed_search_cnt):
            raise CustomMethodNotAllowedException("금일 요청 가능한 횟수를 초과했습니다.")
        
    def get_nrank_searched_count(self):
        memberUtils = MemberPermissionUtils()
        nrankRecordInfoRepository = NRankRecordInfoRepository()
        workspace_info = memberUtils.get_workspace_info()
        ws_id = workspace_info.workspaceId

        date = DateTimeUtils.get_current_datetime()
        start_date = DateTimeUtils.get_start_date(date)
        end_date = DateTimeUtils.get_end_date(date)
        searched_cnt = nrankRecordInfoRepository.search_count_by_period_and_workspace_id(start_date, end_date, ws_id)
        return searched_cnt
    
    def get_subscription_plan_info_for_nrank_search(self):
        memberPermissionUtils = MemberPermissionUtils()

        search_info_dto = WorkspaceNRankSearchInfoDto()
        search_info_dto.search_page_size = memberPermissionUtils.get_nrank_search_page_size()
        search_info_dto.searched_count = self.get_nrank_searched_count()
        search_info_dto.allowed_search_count = memberPermissionUtils.get_nrank_search_allowed_count()
        return search_info_dto.__dict__