from utils import get_db_session
from flask import g

def transactional(**options):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                is_read_only = options.get('read_only') or False
                in_transaction = g.get('in_transaction', None)

                # 트랜잭션에 타지 않았다면
                if(in_transaction is None):
                    g.in_transaction = True
                    g.read_only = is_read_only
                
                if(g.get('read_only', False)):
                    results = func(self, *args, **kwargs)
                    return results
                else:
                    results = func(self, *args, **kwargs)
                    get_db_session().commit()
                    return results    
            except:
                print("==== rollback ====")
                get_db_session().rollback()
                raise
            finally:
                get_db_session().close()
            
        return inner_wrapper
    return outer_wrapper
