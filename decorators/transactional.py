from utils.db.v2.DBUtils import db_session

def transactional(func):
    def wrapper(self, *args, **kwargs):
        results = None
        try:
            results = func(self, *args, **kwargs) or None
            db_session.commit()
            # close 되기 전에 results 반환되어 버림.
            # return results
        except:
            print("==== rollback ====")
            db_session.rollback()
            raise
        finally:
            print("==== close db ====")
            db_session.close()
            return results
        

    return wrapper
