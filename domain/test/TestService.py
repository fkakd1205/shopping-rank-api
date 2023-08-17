import time
# from utils.celery.v1.CeleryUtils import celery
# from utils.celery.v1.CeleryUtils import celery
from exception.types.CustomException import *

class TestService():
    
    # @celery.task
    def celery_test():
        print("celery_test start!!")
        time.sleep(5)
        print("celery_test finish!!")

    def test(self):
        # try:
        # self.inner_test()

        # except Exception as e:
        #     raise e.__class__
        raise CustomDuplicationException('test - service exception!')
    
    # def inner_test(self):
        # raise CustomMethodNotAllowedException('inner test - service exception!')
