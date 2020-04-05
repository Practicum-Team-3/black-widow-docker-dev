from flask import Flask, jsonify, request
from Managers.VagrantManager import VagrantManager
from CeleryApp import createApp, celery
from Entities.Response import Response
from Managers import Tasks
from Managers.DatabaseManager import DatabaseManager
from Entities.Response import Response
import settings

MONGODB_IP = settings.mongodb_ip
MONGODB_PORT = settings.mongodb_port
MONGODB_ROOT_USERNAME = "rootuser"
MONGODB_ROOT_PASSWORD = "your_mongodb_password"
MONGODB_COMPLETE_URL = "mongodb://" + MONGODB_ROOT_USERNAME + ":" + MONGODB_ROOT_PASSWORD + "@" + MONGODB_IP + ":" + MONGODB_PORT

database_manager = DatabaseManager(url= MONGODB_COMPLETE_URL)
vagrant_manager = VagrantManager(database_manager)

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
  task = celery.send_task('Tasks.runVagrantUp', args=[scenario_name])
  response = Response(True, 200, "Pending", task.id)
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