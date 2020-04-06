from flask import Flask, jsonify, request
import requests
from Managers.ScenarioManager import ScenarioManager
from Managers.ConfigManager import ConfigManager

upload_url = ConfigManager().uploadURL()
vagrant_url = ConfigManager().vagrantURL()
scenario_manager = ScenarioManager()

application = Flask(__name__)

@application.route('/upload/filelist')
def getFileList():
  return requests.get('/'.join([upload_url, "fileList"])).json()

@application.route('/upload/deletefile/<file_name>')
def deleteFile(file_name):
  return requests.get('/'.join([upload_url, "deleteFile", file_name])).json()

@application.route('/upload/file', methods=['GET','POST'])
def uploadFile():
  if request.method == 'POST':
      f = request.files['file']
  return requests.post('/'.join([upload_url, "uploadFile"]), files=f).json()

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
  return requests.get('/'.join([vagrant_url, "vagrant", "boxes", "all"])).json()


@application.route('/vagrant/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the vagrant up commands were successfully executed
  """
  return requests.get('/'.join([vagrant_url, "vagrant", scenario_name, "run"])).json()

@application.route('/vagrant/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  """
  Tests network connectivity between two virtual machines
  :param scenario_name: String with the scenario name
  :param source: Source virtual machine
  :param destination: Destination virtual machine
  :return:
  """
  return requests.get('/'.join([vagrant_url, "vagrant", scenario_name, "ping", source, destination])).json()

if __name__=="__main__":
  
  application.run(host='0.0.0.0', port=ConfigManager().widow_app_port)