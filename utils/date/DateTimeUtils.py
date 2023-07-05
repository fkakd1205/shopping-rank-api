from datetime import datetime

class DateTimeUtils():
    
    @staticmethod
    def get_current_datetime():
        return datetime.utcnow()
