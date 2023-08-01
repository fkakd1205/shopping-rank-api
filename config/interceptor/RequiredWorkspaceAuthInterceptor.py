from domain.workspace.dto.WorkspaceAuthTypeDto import WorkspaceAuthTypeDto
from domain.workspace.service.WorkspaceAuthService import WorkspaceAuthService

def required_workspace_auth(**types):
    def outer_wrapper(func):
        def innter_wrapper(self, *args, **kwargs):
            workspace_service = WorkspaceAuthService()
            workspace_auth_type_dto = WorkspaceAuthTypeDto(types)
            workspace_service.get_workspace_auth_info_dto(workspace_auth_type_dto)
            
            return func(self, *args, **kwargs)
        return innter_wrapper
    return outer_wrapper