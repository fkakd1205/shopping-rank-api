from datetime import datetime
from http import HTTPStatus
from dataclasses import dataclass

@dataclass
class MessageDto():
    status = HTTPStatus.BAD_REQUEST.phrase
    status_code = HTTPStatus.BAD_REQUEST.value
    status_message = HTTPStatus.BAD_REQUEST.phrase
    message = None
    memo = None
    data = None
    datetime = str(datetime.now())
        
    def set_status(self, status):
        self.status = status.phrase
        self.status_code = status.value
        self.status_message = status.phrase

    def set_data(self, data):
        self.data = data

    def set_message(self, message):
        self.message = message

    def set_memo(self, memo):
        self.memo = memo
        