from datetime import datetime, timedelta

from exception.types.CustomException import *

class DateTimeUtils():
    
    @staticmethod
    def get_current_datetime():
        return datetime.utcnow()
    
    @staticmethod
    def get_utc_start_date(date):
        if(type(date) != datetime):
            raise CustomNotMatchedFormatException("데이터 형식 변환 오류 : 날짜 타입 데이터가 아닙니다.")
        
        return datetime.strftime(date, "%Y-%m-%d 00:00:00")
    
    
    @staticmethod
    def get_utc_end_date(date):
        if(type(date) != datetime):
            raise CustomNotMatchedFormatException("데이터 형식 변환 오류 : 날짜 타입 데이터가 아닙니다.")
        
        return datetime.strftime(date, "%Y-%m-%d 23:59:59")
