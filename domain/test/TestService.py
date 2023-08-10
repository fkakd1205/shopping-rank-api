import time
# from utils.celery.v1.CeleryUtils import celery
# from utils.celery.v1.CeleryUtils import celery

class TestService():
    
    # @celery.task
    def celery_test():
        print("celery_test start!!")
        time.sleep(5)
        print("celery_test finish!!")

    def test(self):
        # self.celery_test.delay()
        return
