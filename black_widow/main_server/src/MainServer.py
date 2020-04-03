from flask import Flask, jsonify, request
import requests
import settings
from Managers.ScenarioManager import ScenarioManager
from Managers.DatabaseManager import DatabaseManager

ENVIRONMENT_DEBUG = settings.env_debug
VAGRANT_PORT = settings.vagrant_app_port
WIDOW_PORT = settings.widow_app_port
VSERVER_URL = "http://"+ settings.vagrant_host_ip + ":" + VAGRANT_PORT

MONGODB_IP = settings.mongodb_ip
MONGOD_PORT = settings.mongodb_port
MONGODB_USERNAME = settings.mongodb_username
MONGODB_PASSWORD = settings.mongdb_password
MONGODB_ROOT_USERNAME = "rootuser"
MONGODB_ROOT_PASSWORD = "your_mongodb_password"
MONGODB_COMPLETE_URL = "mongodb://" + MONGODB_ROOT_USERNAME + ":" + MONGODB_ROOT_PASSWORD + "@" + MONGODB_IP + ":" + MONGOD_PORT

UPLOAD_IP = '172.18.128.4'
UPLOAD_PORT = '5000'
UPLOAD_URL = 'http://' + UPLOAD_IP + ':' + UPLOAD_PORT

database_manager = DatabaseManager(url= MONGODB_COMPLETE_URL)
scenario_manager = ScenarioManager(db_manager = database_manager)

application = Flask(__name__)

@application.route('/upload/filelist')
def getFileList():
  return requests.get('/'.join([UPLOAD_URL, "fileList"])).json()

@application.route('/upload/deletefile/<file_name>')
def deleteFile(file_name):
  return requests.get('/'.join([UPLOAD_URL, "deleteFile", file_name])).json()

@application.route('/upload/file', methods=['GET','POST'])
def uploadFile():
  if request.method == 'POST':
      f = request.files['file']
  return requests.post('/'.join([UPLOAD_URL, "uploadFile"]), files=f).json()

@application.route('/scenarios/newEmpty/<scenario_name>')
def createScenario(scenario_name):
  """
  Creates a new scenario which includes the folders and the scenario JSON file
  :param scenario_name: String with the scenario name
  :return: True if the new scenario was successfully created
  """
  return jsonify(scenario_manager.newEmptyScenario(scenario_name))

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

@application.route('/scenarios/delete/<scenario_name>')
def deleteScenario(scenario_name):
  """
  Edits a current scenario with a JSON file
  :param scenario_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(scenario_manager.deleteScenario(scenario_name))

@application.route('/vagrant/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context
  :return: A list of string with the available boxes
  """
  return requests.get('/'.join([VSERVER_URL, "vagrant", "boxes", "all"])).json()


@application.route('/vagrant/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the vagrant up commands were successfully executed
  """
  return requests.get('/'.join([VSERVER_URL, "vagrant", scenario_name,"run"])).json()

@application.route('/vagrant/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  """
  Tests network connectivity between two virtual machines
  :param scenario_name: String with the scenario name
  :param source: Source virtual machine
  :param destination: Destination virtual machine
  :return:
  """
  return requests.get('/'.join([VSERVER_URL, "vagrant", scenario_name,"ping", source, destination])).json()

if __name__=="__main__":
  
  application.run(host='0.0.0.0', port=WIDOW_PORT)