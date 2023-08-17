from utils.db.v2.DBUtils import db_session

def using_db(**options):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                results = func(self, *args, **kwargs)
                return results
            finally:
                auto_close = options.get('auto_close', True)
                if(auto_close):
                    db_session.close()

        return inner_wrapper
    return outer_wrapper
