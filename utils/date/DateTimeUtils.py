from datetime import datetime

from exception.types.CustomException import *

class DateTimeUtils():
    
    @staticmethod
    def get_current_datetime():
        return datetime.utcnow()
    
    @staticmethod
    def get_start_date(date):
        if(type(date) == datetime):
            start_date = datetime(date.year, date.month, date.day-1)
            # TODO :: 변경해야 함
            return datetime.strftime(start_date, "%Y-%m-%d 15:00:00")
    
    @staticmethod
    def get_end_date(date):
        if(type(date) == datetime):
            # TODO :: 변경해야 함
            return datetime.strftime(date, "%Y-%m-%d 14:59:59")
