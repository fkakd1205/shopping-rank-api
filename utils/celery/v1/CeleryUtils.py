from celery import Celery

# === Celery setting ===
# app start 될때 한번 실행
# def init_celery():
#     celery = Celery(
#         'app',
#         backend='redis://localhost:6379/0',
#         broker='redis://localhost:6379/0'
#     )

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery

# celery = init_celery()

celery = Celery(
    'app',
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0'
)
