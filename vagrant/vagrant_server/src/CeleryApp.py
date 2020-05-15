from celery import Celery 
from flask import Flask
from Managers.ConfigManager import ConfigManager

redis_url = ConfigManager().redisURL()
celery = Celery(__name__, broker = redis_url, include = ['Managers.VagrantManager'])

def createApp():
    """
    Creates a Celery app
    :return: Celery's app
    """
    app = Flask(__name__)
    app.config['CELERY_BROKER_URL'] = redis_url
    app.config['CELERY_RESULT_BACKEND'] = redis_url
    celery.conf.update(app.config)

    return app