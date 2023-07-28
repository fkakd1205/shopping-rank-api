from utils.db.v2.DBUtils import db_session

def transactional(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
            db_session.commit()
        except:
            print("=== rollback ===")
            db_session.rollback()
            # TODO :: 예외 작성
            raise
        finally:
            db_session.close()

    return wrapper
