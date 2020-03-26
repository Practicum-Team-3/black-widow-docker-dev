from flask import Flask, jsonify, request
import requests
import settings
from Managers.ScenarioManager import ScenarioManager

application = Flask(__name__)
scenario_manager = ScenarioManager()
vserver_url = 'http://'+ settings.vagrant_host_ip + ':' + settings.vagrant_app_port
app_port = settings.vagrant_app_port

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

@application.route('/scenarios/new/<scenario_name>')
def createScenario(scenario_name):
  """
  Creates a new scenario which includes the folders and the scenario JSON file
  :param scenario_name: String with the scenario name
  :return: True if the new scenario was successfully created
  """
  return jsonify(scenario_manager.createScenario(scenario_name))

@application.route('/vagrant/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context
  :return: A list of string with the available boxes
  """
  return requests.get('/'.join([vserver_url, "vagrant", "boxes", "all"])).content

@application.route('/vagrant/<scenario_name>/all')
def createVagrantFiles(scenario_name):
  """
  Create the vagrant files for the existing machines in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the files were successfully created
  """
  return requests.get('/'.join([vserver_url, "vagrant", scenario_name,"all"])).content

@application.route('/vagrant/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the vagrant up commands were successfully executed
  """
  return requests.get('/'.join([vserver_url, "vagrant", scenario_name,"run"])).content

@application.route('/vagrant/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  """
  Tests network connectivity between two virtual machines
  :param scenario_name: String with the scenario name
  :param source: Source virtual machine
  :param destination: Destination virtual machine
  :return:
  """
  return requests.get('/'.join([vserver_url, "vagrant", scenario_name,"ping", source, destination])).content

if __name__=="__main__":
  application.run('0.0.0.0', app_port)