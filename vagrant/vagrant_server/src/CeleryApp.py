from celery import Celery 
from flask import Flask
from Managers.FileManager import FileManager
from Managers.ScenarioManager import ScenarioManager
from Entities.VagrantFile import VagrantFile
from Entities.Response import Response

celery = Celery(__name__, broker='redis://localhost:9090/0', include=['Managers.Tasks'])

file_manager = FileManager()
scenario_manager = ScenarioManager()
vagrant_file = VagrantFile()
response = Response() 

def createApp():
    app = Flask(__name__)
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:9090/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:9090/0'
    celery.conf.update(app.config)

    return app