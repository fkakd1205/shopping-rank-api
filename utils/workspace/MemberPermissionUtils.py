from flask import g

class MemberPermissionUtils():
    def get_workspace_info(self):
        workspace_info = g.get('workspace_auth_info')
        
        # TODO :: 예외처리
        if(workspace_info is None): raise

        return workspace_info