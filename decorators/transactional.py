from utils import db_session

def transactional(func):
    def wrapper(self, *args, **kwargs):
        try:
            results = func(self, *args, **kwargs)
            db_session.commit()
            return results
        except:
            print("==== rollback ====")
            db_session.rollback()
            raise
        finally:
            print("==== close db ====")
            db_session.close()

    return wrapper
