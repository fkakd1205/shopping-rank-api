from flask import request, g
import requests
import json
from http import HTTPStatus

from domain.workspace.dto.WorkspaceAuthInfoDto import WorkspaceAuthInfoDto
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository

from exception.types.CustomException import *

from utils.cookie.CustomCookieUtils import CustomCookieUtils
from config.key.prod.ProductionConfig import origin
from utils.date.DateTimeUtils import DateTimeUtils
from utils.workspace.MemberPermissionUtils import MemberPermissionUtils

class WorkspaceAuthService():
    
    def get_workspace_auth_info_dto(self, check_permission_body):
        headers = request.headers
        cookies = request.cookies

        ws_id = headers['wsId']
        jwt_token_cookie = cookies.get(CustomCookieUtils.COOKIE_NAME_ACCESS_TOKEN)
        
        request_url = origin['auth-api'] + '/auth/v1/workspaces/checkPermissions'
        request_headers = {
            'wsId': ws_id,
            'referer': origin['store-rank-api'],
            'Content-Type': 'application/json'
        }
        request_cookies = {CustomCookieUtils.COOKIE_NAME_ACCESS_TOKEN: jwt_token_cookie}

        response = requests.post(url=request_url, 
            headers=request_headers,
            cookies=request_cookies,
            data=json.dumps(check_permission_body.__dict__)
        )

        if(response.status_code != 200):
            self.request_error_handler(response)
            return

        object = response.json()
        data = object['data']
        info_dto = WorkspaceAuthInfoDto(data)

        g.workspace_auth_info = info_dto

    def request_error_handler(self, response):
        status_code = response.status_code
        object = response.json()

        if (status_code == HTTPStatus.UNAUTHORIZED):
            raise CustomInvalidUserException("로그인이 필요한 서비스 입니다.")
        elif (status_code == HTTPStatus.FORBIDDEN):
            memo = object['memo'] if object and object['memo'] else "접근 권한이 없습니다."
            raise CustomAccessDeniedPermissionException(memo)
        elif (status_code == HTTPStatus.BAD_REQUEST):
            message = object['message'] if object and object['message'] else "undefined"

            if(message == "must_check_parameters"):
                memo = object['memo'] if object and object['memo'] else "알 수 없는 에러."
                raise CustomMethodNotAllowedException("서버 게이트웨이 에러. 관리자에게 문의해 주세요.")
            
            raise CustomMethodNotAllowedException("요청 양식이 올바른지 확인해 주세요.")
        else:
            raise CustomMethodNotAllowedException("알 수 없는 에러가 발생했습니다.")

    def check_nrank_search_allowed_count(self):
        memberUtils = MemberPermissionUtils()
        workspace_info = memberUtils.get_workspace_info()
        ws_id = workspace_info.workspaceId

        nrank_record_info_repository = NRankRecordInfoRepository()
        date = DateTimeUtils.get_current_datetime()
        start_date = DateTimeUtils.get_start_date(date)
        end_date = DateTimeUtils.get_end_date(date)
        searched_cnt = nrank_record_info_repository.search_count_by_period_and_workspace_id(start_date, end_date, ws_id)

        allowed_search_cnt = memberUtils.get_nrank_search_allowed_count()
        if(searched_cnt >= allowed_search_cnt):
            raise CustomMethodNotAllowedException("금일 요청 가능한 횟수를 초과했습니다.")
    
    def get_nrank_search_page_size(self):
        memberUtils = MemberPermissionUtils()
        allowed_page_size = memberUtils.get_nrank_search_page_size()
        return allowed_page_size
        
        
        
        
        
        