from celery import Celery, Task

# V1
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

# V2
# celery = Celery(
#     'app',
#     # backend='redis://localhost:6379/0',
#     broker='redis://localhost:6379/0'
# )

# V3
def init_celery(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery_app = Celery('app', broker='redis://localhost:6379/0', task_cls=FlaskTask)
    celery_app.config_from_object('app')
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


