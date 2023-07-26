from utils.db.v2.DBUtils import db_session

def transactional(func):
    def wrapper(self, *args):
        try:
            func(self, *args)
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            print("close")
            db_session.close()

    return wrapper
