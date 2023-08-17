from flask import g

from exception.types.CustomException import CustomInvalidWorkspaceException

class MemberPermissionUtils():
    def get_workspace_info(self):
        workspace_info = g.get('workspace_auth_info')
        if(workspace_info is None): raise CustomInvalidWorkspaceException("워크스페이스 권한이 필요한 서비스 입니다.")

        return workspace_info
