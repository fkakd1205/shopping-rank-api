from flask import g

class MemberPermissionUtils():
    def get_workspace_id(self):
        workspace_id = g.get('workspace_id')
        # TODO :: 예외처리
        if(workspace_id is None): raise

        return workspace_id