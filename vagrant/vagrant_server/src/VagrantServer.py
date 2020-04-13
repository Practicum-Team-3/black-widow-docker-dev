from flask import jsonify, request, url_for
from Managers.VagrantManager import VagrantManager
from Entities.Response import Response
from CeleryApp import createApp, celery

vagrant_manager = VagrantManager()

application = createApp()

@application.route('/vagrant/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context
  :return: A list of string with the available boxes
  """
  return jsonify(vagrant_manager.getAvailableBoxes())

@application.route('/vagrant/boxes/add', methods = ['POST'])
def addBoxByName():
  box_name = request.get_json()['box_name']
  task = celery.send_task('VagrantManager.addBoxByName', args=[box_name])
  response = Response(True, "Sent to task queue", task.state, task.id)
  return jsonify(response.dictionary())

@application.route('/vagrant/boxes/remove', methods = ['POST'])
def removeBoxByName():
  box_name = request.get_json()['box_name']
  task = celery.send_task('VagrantManager.removeBoxByName', args=[box_name])
  response = Response(True, "Sent to task queue", task.state, task.id)
  return jsonify(response.dictionary())

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

@application.route('/vagrant/manage/<scenario_name>/<machine_name>/<command>')
def vagrantCommand(scenario_name, machine_name, command):
  return jsonify(vagrant_manager.vagrantMachineCommand(scenario_name, machine_name, command))

@celery.task(bind = True)
def getTaskStatus(self, task_id):
    return self.AsyncResult(task_id)


@application.route('/vagrant/taskStatus/<task_id>')
def taskstatus(task_id):
    task = getTaskStatus(task_id)
    status = ""
    if task.state == 'PENDING':

        status = task.state
        body = {
            'state': task.state,
            'current': 0,
            'total': 1
        }
    elif task.state != 'FAILURE':

        status = "IN_PROGRESS"
        status = task.info.get('status', '')
        body = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
        }
        if 'result' in task.info:
            body['result'] = task.info['result']
    else:
        # something went wrong in the background job
        body = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }

    response = Response(True, "Task status", status, task_id)
    response.setBody(body)
    return jsonify(response.dictionary())


if __name__=="__main__":
  application.run('0.0.0.0')