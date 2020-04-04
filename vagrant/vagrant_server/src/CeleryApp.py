from celery import Celery 
from flask import Flask
from Managers.FileManager import FileManager
from Managers.ScenarioManager import ScenarioManager
from Entities.VagrantFile import VagrantFile
from Entities.Response import Response
import settings

REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port

REDIS_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
celery = Celery(__name__, broker = REDIS_URL, include = ['Managers.Tasks'])

file_manager = FileManager()
scenario_manager = ScenarioManager()
vagrant_file = VagrantFile()
response = Response() 

def createApp():
    app = Flask(__name__)
    app.config['CELERY_BROKER_URL'] = REDIS_URL
    app.config['CELERY_RESULT_BACKEND'] = REDIS_URL
    celery.conf.update(app.config)

    return app