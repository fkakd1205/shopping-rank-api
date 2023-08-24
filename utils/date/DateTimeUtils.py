from datetime import datetime

from exception.types.CustomException import *

class DateTimeUtils():
    
    @staticmethod
    def get_current_datetime():
        return datetime.utcnow()
    
    @staticmethod
    def get_start_date(date):
        if(type(date) != datetime):
            raise CustomNotMatchedFormatException("데이터 형식 변환 오류 : 날짜 타입 데이터가 아닙니다.")
        
        start_date = datetime(date.year, date.month, date.day-1) 
        return datetime.strftime(start_date, "%Y-%m-%d 15:00:00")
    
    
    @staticmethod
    def get_end_date(date):
        if(type(date) != datetime):
            raise CustomNotMatchedFormatException("데이터 형식 변환 오류 : 날짜 타입 데이터가 아닙니다.")
        
        return datetime.strftime(date, "%Y-%m-%d 14:59:59")
