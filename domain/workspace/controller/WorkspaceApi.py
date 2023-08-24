from flask_restx import Namespace, Resource
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.workspace.service.WorkspaceService import WorkspaceService

from enums.WorkspaceAccessTypeEnum import WorkspaceAccessTypeEnum
from decorators import *

WorkspaceApi = Namespace('WorkspaceApi')

@WorkspaceApi.route('/nrank-search-info', methods=['GET'])
class WorkspaceRelatedNRankSearchInfo(Resource):

    @required_login
    @required_workspace_auth(checkAccessTypeFlag = True, requiredAccessTypes = {
        WorkspaceAccessTypeEnum.SALES_ANALYSIS_SEARCH
    })
    def get(self):
        message = MessageDto()

        workspaceService = WorkspaceService()
        message.set_data(workspaceService.get_subscription_plan_info_for_nrank_search())
        message.set_status(HTTPStatus.OK)
        message.set_message("success")

        return message.__dict__, message.status_code