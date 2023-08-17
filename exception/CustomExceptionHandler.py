from http import HTTPStatus

from exception.types.CustomException import *
from domain.message.dto.MessageDto import MessageDto

def CustomExceptionHandler(app):
    message = MessageDto()

    # 1. Duplication Exception
    @app.errorhandler(CustomDuplicationException)
    def CustomDuplicationExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("data_duplication")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 2. Invalid User Exception ()
    @app.errorhandler(CustomInvalidValueException)
    def CustomInvalidValueExceptionHanlder(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("invalid_value")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 3. Not Found Exception
    @app.errorhandler(CustomNotFoundException)
    def CustomNotFoundExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.NOT_FOUND)
        message.set_message("not found")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 4. Method Not Allowed Exception
    @app.errorhandler(CustomMethodNotAllowedException)
    def CustomMethodNotAllowedExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.METHOD_NOT_ALLOWED)
        message.set_message("not found")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 5. Invalid User Exception
    @app.errorhandler(CustomInvalidUserException)
    def CustomInvalidUserExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.UNAUTHORIZED)
        message.set_message("invalid_user")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 6. Invalid Workspace Exception
    @app.errorhandler(CustomInvalidWorkspaceException)
    def CustomInvalidWorkspaceExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("invalid_workspace")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 7. Access Denied Permission Exception
    @app.errorhandler(CustomAccessDeniedPermissionException)
    def CustomAccessDeniedPermissionExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.UNAUTHORIZED)
        message.set_message("invalid_user")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 8. Timeout Exception
    @app.errorhandler(CustomTimeoutException)
    def CustomTimeoutExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("timeout")
        message.set_memo(str(e))
        return message.__dict__, message.status_code    
    