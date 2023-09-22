from utils import get_db_session
from flask import g

def transactional(**options):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                # # == V1 ==
                # is_read_only = False

                # # 이미 g객체의 read_only가 설정되어 있다면 pass
                # if(g.get('read_only') is None):
                #     is_read_only = options.get('read_only') or False
                #     g.read_only = is_read_only

                # if(is_read_only):
                #     slave_db_session.execute(text("SET TRANSACTION READ ONLY"))
                #     results = func(self, *args, **kwargs)
                #     return results
                # else:
                #     results = func(self, *args, **kwargs)
                #     db_session.commit()
                #     return results

                # # == V2 ==
                # # TODO :: 데몬쓰레드에서 g 객체 사용 불가
                is_read_only = options.get('read_only') or False
                in_transaction = g.get('in_transaction', None)

                # 트랜잭션에 타지 않았다면
                if(in_transaction is None):
                    g.in_transaction = True
                    g.read_only = is_read_only
                
                if(g.get('read_only', False)):
                    # get_db_session().execute(text("SET TRANSACTION READ ONLY"))
                    results = func(self, *args, **kwargs)
                    return results
                else:
                    results = func(self, *args, **kwargs)
                    get_db_session().commit()
                    return results

                # V3
                # global thread_local
                # in_transaction = getattr(thread_local, 'in_transaction', None)
                # is_read_only = options.get('read_only') or False

                # # 루트 트랜잭션에서 이라면 in_transaction / read_only 설정
                # if(in_transaction is None):
                #     thread_local.in_transaction = True
                #     thread_local.read_only = is_read_only
                
                # # 루트 트랜잭션에서 설정된 thread local 변수에 따라 master / slave db 설정
                # if(getattr(thread_local, 'read_only', False)):
                #     # get_db_session().execute(text("SET TRANSACTION READ ONLY"))
                #     results = func(self, *args, **kwargs)
                #     return results
                # else:
                #     results = func(self, *args, **kwargs)
                #     get_db_session().commit()
                #     return results
            except:
                print("==== rollback ====")
                get_db_session().rollback()
                raise
            finally:
                print("==== close db ====")
                get_db_session().close()
                # 루트 트랜잭션이 여러개라면 하나의 작업이 끝나고 in_transaction 초기화
                # thread_local.in_transaction = None
                # g.in_transaction = None
            
        return inner_wrapper
    return outer_wrapper
