from datetime import datetime
from http import HTTPStatus

class MessageDto():
    def __init__(self):
        self.status = HTTPStatus.BAD_REQUEST.phrase
        self.status_code = HTTPStatus.BAD_REQUEST.value
        self.status_essage = HTTPStatus.BAD_REQUEST.phrase
        self.message = None
        self.memo = None
        self.data = None
        self.datetime = str(datetime.now())

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
        