from celery import Celery 
from flask import Flask
from Managers.FileManager import FileManager
from Managers.ScenarioManager import ScenarioManager
from Managers.DatabaseManager import DatabaseManager
from Entities.VagrantFile import VagrantFile
from Entities.Response import Response
import settings

REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port

REDIS_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
celery = Celery(__name__, broker = REDIS_URL, include = ['Managers.Tasks'])

MONGODB_IP = settings.mongodb_ip
MONGODB_PORT = settings.mongodb_port
MONGODB_ROOT_USERNAME = "rootuser"
MONGODB_ROOT_PASSWORD = "your_mongodb_password"
MONGODB_COMPLETE_URL = "mongodb://" + MONGODB_ROOT_USERNAME + ":" + MONGODB_ROOT_PASSWORD + "@" + MONGODB_IP + ":" + MONGODB_PORT

database_manager = DatabaseManager(url= MONGODB_COMPLETE_URL)
file_manager = FileManager()
scenario_manager = ScenarioManager(db_manager = database_manager)
vagrant_file = VagrantFile()
response = Response()

def createApp():
    app = Flask(__name__)
    app.config['CELERY_BROKER_URL'] = REDIS_URL
    app.config['CELERY_RESULT_BACKEND'] = REDIS_URL
    celery.conf.update(app.config)

    return app