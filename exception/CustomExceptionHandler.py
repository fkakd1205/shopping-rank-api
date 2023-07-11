from http import HTTPStatus

from exception.types.CustomDuplicationException import CustomDuplicationException
from domain.message.dto.MessageDto import MessageDto

def CustomExceptionHandler(app):
    message = MessageDto()

    # snake to camel 적용 전. 추후에 이 과정 제거 예정이므로
    @app.errorhandler(CustomDuplicationException)
    def CustomDuplicationExceptionHandler(e):
        message.set_data(None)
        message.set_status(HTTPStatus.BAD_REQUEST)
        message.set_message("data_duplication")
        message.set_memo(str(e))
        return message.__dict__, message.status_code