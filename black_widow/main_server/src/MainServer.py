from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import requests
import settings
from Managers.ScenarioManager import ScenarioManager

ENVIRONMENT_DEBUG = settings.env_debug
VAGRANT_PORT = settings.vagrant_app_port
WIDOW_PORT = settings.widow_app_port
VSERVER_URL = "http://"+ settings.vagrant_host_ip + ":" + VAGRANT_PORT

MONGOD_IP = settings.mongodb_ip
MONGOD_PORT = settings.mongodb_port

DB_NAME = settings.db_name
MONGODB_USERNAME = settings.mongodb_username
MONGODB_PASSWORD = settings.mongdb_password
MONGODB_URL = "mongodb://" + MONGOD_IP + ":" + MONGOD_PORT
MONGODB_HOSTNAME = settings.mongodb_hostname


application = Flask(__name__)
application.config["MONGO_URI"] = "mongodb://" + MONGODB_USERNAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOSTNAME + ":" + MONGOD_PORT + "/" + DB_NAME

mongo = PyMongo(application)
db = mongo.db

scenario_manager = ScenarioManager()



@application.route('/scenarios/all')
def getScenarios():
  """
  Gets the available scenarios
  :return: A list of strings with the available scenarios
  """
  return jsonify(scenario_manager.getScenarios())

@application.route('/scenarios/<scenario_name>')
def getScenario(scenario_name):
  """
  Gets the scenario as a JSON file
  :param scenario_name: String with the scenario name
  :return: JSON file with the scenario info
  """
  return jsonify(scenario_manager.getScenario(scenario_name))

@application.route('/scenarios/edit', methods = ['POST'])
def editScenario():
  """
  Edits a current scenario with a JSON file
  :param scenario_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(scenario_manager.editScenario(request.get_json()))


@application.route('/vagrant/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context
  :return: A list of string with the available boxes
  """
  return requests.get('/'.join([VSERVER_URL, "vagrant", "boxes", "all"])).content

@application.route('/vagrant/<scenario_name>/all')
def createVagrantFiles(scenario_name):
  """
  Create the vagrant files for the existing machines in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the files were successfully created
  """
  return requests.get('/'.join([VSERVER_URL, "vagrant", scenario_name,"all"])).content

@application.route('/vagrant/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the vagrant up commands were successfully executed
  """
  return requests.get('/'.join([VSERVER_URL, "vagrant", scenario_name,"run"])).content

@application.route('/vagrant/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  """
  Tests network connectivity between two virtual machines
  :param scenario_name: String with the scenario name
  :param source: Source virtual machine
  :param destination: Destination virtual machine
  :return:
  """
  return requests.get('/'.join([VSERVER_URL, "vagrant", scenario_name,"ping", source, destination])).content

if __name__=="__main__":
  
  application.run(host='0.0.0.0', port=WIDOW_PORT)