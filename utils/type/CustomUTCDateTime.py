from datetime import datetime

class CustomUTCDateTime():

    @staticmethod
    def convert_timezone_format(value):
        if (value is not None) & (type(value) is datetime):
            # 데이터베이스에서 datetime 값 형식 변경
            # strftime : datetime을 원하는 형식의 string으로 변경해 리턴
            value = value.strftime("%Y-%m-%dT%H:%M:%SZ")
        return value
