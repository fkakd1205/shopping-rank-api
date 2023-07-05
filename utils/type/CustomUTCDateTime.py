from sqlalchemy.types import TypeDecorator, DateTime

# UTC로 표현하기 위한 커스텀 타입 정의
class CustomUTCDateTime(TypeDecorator):
    impl = DateTime

    def process_result_value(self, value, dialect):
        if value is not None:
            # 데이터베이스에서 받은 값에 타임존 설정
            value = value.strftime("%Y-%m-%dT%H:%M:%SZ")
        return value