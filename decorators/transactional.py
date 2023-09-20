from utils import db_session, slave_db_session
from sqlalchemy import text
from flask import g

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

def transactional2(**options):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                is_read_only = False

                # 이미 g객체의 read_only가 설정되어 있다면 pass
                if(g.get('read_only') is None):
                    is_read_only = options.get('read_only') or False
                    g.read_only = is_read_only
                
                if(is_read_only):
                    slave_db_session.execute(text("SET TRANSACTION READ ONLY"))
                    results = func(self, *args, **kwargs)
                    # slave_db_session.commit()
                    return results
                else:
                    results = func(self, *args, **kwargs)
                    db_session.commit()
                    return results
            except:
                print("==== rollback ====")
                slave_db_session.rollback()
                db_session.rollback()
                raise
            finally:
                print("==== close db ====")
                slave_db_session.close()
                db_session.close()
        return inner_wrapper
    return outer_wrapper
