from flask import jsonify
from CeleryApp import createApp, celery
from Managers.VagrantManager import VagrantManager
from Entities.Response import Response

vagrant_manager = VagrantManager()

application = createApp()

@application.route('/vagrant/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context
  :return: A list of string with the available boxes
  """
  return jsonify(vagrant_manager.getAvailableBoxes())


@application.route('/vagrant/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the vagrant up commands were successfully executed
  """
  task = celery.send_task('VagrantManager.runVagrantUp', args=[scenario_name])
  response = Response(True, "Sent to task queue", "Pending", task.id)
  return jsonify(response.dictionary())

@application.route('/vagrant/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  """
  Tests network connectivity between two virtual machines
  :param scenario_name: String with the scenario name
  :param source: Source virtual machine
  :param destination: Destination virtual machine
  :return:
  """
  return jsonify(vagrant_manager.testNetworkPing(scenario_name, source, destination))

if __name__=="__main__":
  application.run('0.0.0.0')