from http import HTTPStatus

from exception.types.CustomException import *
from domain.message.dto.MessageDto import MessageDto

def CustomExceptionHandler(api):
    message = MessageDto()

    # 1. Duplication Exception
    @api.errorhandler(CustomDuplicationException)
    def CustomDuplicationExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("data_duplication")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 2. Invalid User Exception
    @api.errorhandler(CustomInvalidValueException)
    def CustomInvalidValueExceptionHanlder(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("invalid_value")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 3. Not Found Exception
    @api.errorhandler(CustomNotFoundException)
    def CustomNotFoundExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.NOT_FOUND)
        message.set_message("not found")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 4. Method Not Allowed Exception
    @api.errorhandler(CustomMethodNotAllowedException)
    def CustomMethodNotAllowedExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.METHOD_NOT_ALLOWED)
        message.set_message("not found")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 5. Invalid User Exception
    @api.errorhandler(CustomInvalidUserException)
    def CustomInvalidUserExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.UNAUTHORIZED)
        message.set_message("invalid_user")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 6. Invalid Workspace Exception
    @api.errorhandler(CustomInvalidWorkspaceException)
    def CustomInvalidWorkspaceExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("invalid_workspace")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 7. Access Denied Permission Exception
    @api.errorhandler(CustomAccessDeniedPermissionException)
    def CustomAccessDeniedPermissionExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.UNAUTHORIZED)
        message.set_message("invalid_user")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 8. Timeout Exception
    @api.errorhandler(CustomTimeoutException)
    def CustomTimeoutExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("timeout")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    
    # 9. Not Matched Format Exception
    @api.errorhandler(CustomNotMatchedFormatException)
    def CustomNotMatchedFormatExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("not matched format")
        message.set_memo(str(e))
        return message.__dict__, message.status_code
    