from flask import request, g
import requests
import json
from http import HTTPStatus

from domain.workspace.dto.WorkspaceAuthTypeDto import WorkspaceAuthTypeDto
from domain.workspace.dto.WorkspaceAuthInfoDto import WorkspaceAuthInfoDto

from exception.types.CustomException import *

from utils.cookie.CustomCookieUtils import CustomCookieUtils
from config.key.prod.ProductionConfig import origin

class WorkspaceAuthService():
    
    def get_workspace_auth_info_dto(self, workspace_auth_type):
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

        auth_type_dto = WorkspaceAuthTypeDto.CamelCase()
        auth_type_dto.checkMasterPermissionFlag = workspace_auth_type.check_master_permission_flag
        auth_type_dto.checkAccessTypeFlag = workspace_auth_type.check_access_type_flag
        auth_type_dto.checkSubscriptionPlanFlag = workspace_auth_type.check_subscription_plan_flag
        auth_type_dto.requiredAccessTypes = list(map(lambda type: type.value, workspace_auth_type.required_access_types))
        auth_type_dto.requiredSubscriptionPlans = list(map(lambda plan: plan.value, workspace_auth_type.required_subscription_plans))

        response = requests.post(url=request_url, 
            headers=request_headers,
            cookies=request_cookies,
            data=json.dumps(auth_type_dto.__dict__)
        )

        if(response.status_code != 200):
            self.request_error_handler(response)
            return

        object = response.json()
        data = object['data']

        info_dto = WorkspaceAuthInfoDto()
        info_dto.workspace_member_id = data['workspaceMemberId']
        info_dto.template_use_yn = data['templateUseYn']
        info_dto.is_master = data['master']
        info_dto.workspace_auth_items = list(map(lambda item: WorkspaceAuthInfoDto.WorkspaceAuthItem(item), data['workspaceAuthItems']))
        info_dto.workspace_id = data['workspaceId']
        info_dto.subscription_plan = data['subscriptionPlan']
        info_dto.subscription_expiry_date = data['subscriptionExpiryDate']

        g.workspace_auth_info = info_dto
        g.workspace_id = info_dto.workspace_id

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
