from flask import g

from exception.types.CustomException import CustomInvalidWorkspaceException
from enums.WorkspaceSubscriptionPlanEnum import WorkspaceSubscriptionPlanEnum

class MemberPermissionUtils():
    def get_workspace_info(self):
        workspace_info = g.get('workspace_auth_info')
        if(workspace_info is None): raise CustomInvalidWorkspaceException("워크스페이스 권한이 필요한 서비스 입니다.")

        return workspace_info
    
    def get_nrank_search_allowed_count(self):
        workspace_info = self.get_workspace_info()
        plan = WorkspaceSubscriptionPlanEnum(workspace_info.subscriptionPlan)

        results = {
            WorkspaceSubscriptionPlanEnum.NONE: 0,
            WorkspaceSubscriptionPlanEnum.PRIVATE: 2,
            WorkspaceSubscriptionPlanEnum.PUBLIC: 10
        }
        return results[plan]
        
    def get_nrank_search_page_size(self):
        workspace_info = self.get_workspace_info()
        plan = WorkspaceSubscriptionPlanEnum(workspace_info.subscriptionPlan)

        results = {
            WorkspaceSubscriptionPlanEnum.NONE: 0,
            WorkspaceSubscriptionPlanEnum.PRIVATE: 1,   # 80위
            WorkspaceSubscriptionPlanEnum.PUBLIC: 2     # 160위
        }
        return results[plan]