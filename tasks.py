from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

@app.task
def add(x, y):
    return x + y

# import os
# app.conf.update(BROKER_URL=os.environ['REDISGREEN_URL'],
#                 CELERY_RESULT_BACKEND=os.environ['REDISGREEN_URL'])