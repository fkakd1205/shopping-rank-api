from domain.workspace.dto.CheckPermissionBodyDto import CheckPermissionBodyDto
from domain.workspace.service.WorkspaceAuthService import WorkspaceAuthService

def required_workspace_auth(**types):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            workspaceService = WorkspaceAuthService()
            workspace_auth_type_dto = CheckPermissionBodyDto(types)
            workspaceService.get_workspace_auth_info_dto(workspace_auth_type_dto)
            
            return func(self, *args, **kwargs)
        return inner_wrapper
    return outer_wrapper