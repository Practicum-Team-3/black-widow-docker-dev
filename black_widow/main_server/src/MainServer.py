from flask import Flask, jsonify, request, render_template,redirect, url_for
import requests
from Managers.ScenarioManager import ScenarioManager
from Managers.ExploitManager import ExploitManager
from Managers.VulnerabilityManager import VulnerabilityManager
from Managers.ConfigManager import ConfigManager

upload_url = ConfigManager().uploadURL()
vagrant_url = ConfigManager().vagrantURL()
scenario_manager = ScenarioManager()
exploit_manager = ExploitManager()
vulnerability_manager = VulnerabilityManager()

application = Flask(__name__)

#________________REMOVE THIS AFTER TESTING_____________
@application.route('/test', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    return redirect(url_for('index'))

@application.route('/longtask')
def longtask():

    toReturn = requests.get('/'.join([vagrant_url, "longtask"])).json()
    print(toReturn)
    return toReturn

#Upload files
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

#Scenarios
@application.route('/scenarios/newEmpty/<scenario_name>')
def createScenario(scenario_name):
  """
  Creates a new scenario which includes the folders and the scenario JSON file
  :param scenario_name: String with the scenario name
  :return: True if the new scenario was successfully created
  """
  return jsonify(scenario_manager.newEmpty(scenario_name))

@application.route('/scenarios/all')
def getScenarios():
  """
  Gets the available scenarios
  :return: A list of strings with the available scenarios
  """
  return jsonify(scenario_manager.getAll())

@application.route('/scenarios/<scenario_name>')
def getScenario(scenario_name):
  """
  Gets the scenario as a JSON file
  :param scenario_name: String with the scenario name
  :return: JSON file with the scenario info
  """
  return jsonify(scenario_manager.getOne(scenario_name))

@application.route('/scenarios/edit', methods = ['POST'])
def editScenario():
  """
  Edits a current scenario with a JSON file
  :param scenario_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(scenario_manager.editOne(request.get_json()))

@application.route('/scenarios/delete/<scenario_name>')
def deleteScenario(scenario_name):
  """
  Edits a current scenario with a JSON file
  :param scenario_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(scenario_manager.deleteOne(scenario_name))

#Exploits
@application.route('/exploits/newEmpty/<exploit_name>')
def createExploit(exploit_name):
  """
  Creates a new scenario which includes the folders and the scenario JSON file
  :param scenario_name: String with the scenario name
  :return: True if the new scenario was successfully created
  """
  return jsonify(exploit_manager.newEmpty(exploit_name))

@application.route('/exploits/all')
def getExploits():
  """
  Gets the available scenarios
  :return: A list of strings with the available scenarios
  """
  return jsonify(exploit_manager.getAll())

@application.route('/exploits/<exploit_name>')
def getExploit(exploit_name):
  """
  Gets the scenario as a JSON file
  :param exploit_name: String with the scenario name
  :return: JSON file with the scenario info
  """
  return jsonify(exploit_manager.getOne(exploit_name))

@application.route('/exploits/edit', methods = ['POST'])
def editExploit():
  """
  Edits a current scenario with a JSON file
  :param scenario_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(exploit_manager.editOne(request.get_json()))

@application.route('/exploits/delete/<exploit_name>')
def deleteExploit(exploit_name):
  """
  Edits a current scenario with a JSON file
  :param exploit_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(exploit_manager.deleteOne(exploit_name))

#Vulnerabilities
@application.route('/vulnerabilities/newEmpty/<vulnerability_name>')
def createVulnerability(vulnerability_name):
  """
  Creates a new scenario which includes the folders and the scenario JSON file
  :param scenario_name: String with the scenario name
  :return: True if the new scenario was successfully created
  """
  return jsonify(vulnerability_manager.newEmpty(vulnerability_name))

@application.route('/vulnerabilities/all')
def getVulnerabilities():
  """
  Gets the available scenarios
  :return: A list of strings with the available scenarios
  """
  return jsonify(vulnerability_manager.getAll())

@application.route('/vulnerabilities/<vulnerability_name>')
def getVulnerability(vulnerability_name):
  """
  Gets the scenario as a JSON file
  :param vulnerability_name: String with the scenario name
  :return: JSON file with the scenario info
  """
  return jsonify(vulnerability_manager.getOne(vulnerability_name))

@application.route('/vulnerabilities/edit', methods = ['POST'])
def editVulnearbility():
  """
  Edits a current scenario with a JSON file
  :param scenario_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(vulnerability_manager.editOne(request.get_json()))

@application.route('/vulnerabilities/delete/<vulnerability_name>')
def deleteVulnerability(vulnerability_name):
  """
  Edits a current scenario with a JSON file
  :param vulnerability_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(vulnerability_manager.deleteOne(vulnerability_name))

#Vagrant
@application.route('/vagrant/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context
  :return: A list of string with the available boxes
  """
  return requests.get('/'.join([vagrant_url, "vagrant", "boxes", "all"])).json()

@application.route('/vagrant/boxes/add', methods = ['POST'])
def addBoxByName():
  json_file = request.get_json()
  return requests.post('/'.join([vagrant_url, "vagrant", "boxes", "add"]), json = json_file).json()

@application.route('/vagrant/boxes/remove', methods = ['POST'])
def removeBoxByName():
  json_file = request.get_json()
  return requests.post('/'.join([vagrant_url, "vagrant", "boxes", "remove"]), json = json_file).json()

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

@application.route('/vagrant/taskStatus/<task_id>')
def getTaskStatus(task_id):
  """
  Requests the status of an ongoing task from the VagranServer
  :param task_id: Task ID given by Celery
  :return: a json response that denotes the status of the task
  """
  return requests.get('/'.join([vagrant_url, "vagrant", "taskStatus", task_id])).json()

if __name__=="__main__":
  
  application.run(host='0.0.0.0', port=ConfigManager().widow_app_port)