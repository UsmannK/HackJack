from celery import Celery
from flask import Flask

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://x:a31d764007e14695bbfe744355d7505e@handsome-sycamore-6643.redisgreen.net:11042/',
    CELERY_RESULT_BACKEND='redis://x:a31d764007e14695bbfe744355d7505e@handsome-sycamore-6643.redisgreen.net:11042/'
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def add(x, y):
    return x + y