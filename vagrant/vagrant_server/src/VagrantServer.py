from flask import jsonify, request, url_for
from Managers.VagrantManager import VagrantManager
from Entities.Response import Response
from CeleryApp import createApp, celery

vagrant_manager = VagrantManager()
application = createApp()

@application.route('/vagrant/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context.
  :return: A list of string with the available boxes
  """
  return jsonify(vagrant_manager.getAvailableBoxes())

@application.route('/vagrant/boxes/add', methods = ['POST'])
def addBoxByName():
  """
  Adds a box by name inside Vagrant.
  :return: Response object containing the status of the request
  """
  box_name = request.get_json()['box_name']
  task = celery.send_task('VagrantManager.addBoxByName', args=[box_name])
  response = Response(True, "Sent to task queue", task.state, task.id)
  return jsonify(response.dictionary())

@application.route('/vagrant/boxes/remove', methods = ['POST'])
def removeBoxByName():
  """
  Removes a box by name from Vagrant.
  :return: Response object containing the status of the request
  """
  box_name = request.get_json()['box_name']
  task = celery.send_task('VagrantManager.removeBoxByName', args=[box_name])
  response = Response(True, "Sent to task queue", task.state, task.id)
  return jsonify(response.dictionary())

@application.route('/vagrant/boxes/addByOVAFile', methods=['POST'])
def addBoxByOVAFile():
  """
  Adds a box by using an OVA file.
  :return: Response object containing the status of the request
  """
  file_name = request.get_json()['file_name']
  task = celery.send_task('VagrantManager.addBoxByOVAFile', args=[file_name])
  response = Response(True, "Sent to task queue", task.state, task.id)
  return jsonify(response.dictionary())

@application.route('/vagrant/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario.
  :param scenario_name: String with the scenario name
  :return: True if the vagrant up commands were successfully executed
  """
  task = celery.send_task('VagrantManager.runVagrantUp', args=[scenario_name])
  response = Response(True, "Sent to task queue", "Pending", task.id)
  return jsonify(response.dictionary())

@application.route('/vagrant/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  """
  Tests network connectivity between two virtual machines.
  :param scenario_name: String with the scenario name
  :param source: Source virtual machine
  :param destination: Destination virtual machine
  :return: Response object containing the status of the request
  """
  return jsonify(vagrant_manager.testNetworkPing(scenario_name, source, destination))

@application.route('/vagrant/manage/<scenario_name>/<machine_name>/<command>')
def vagrantCommand(scenario_name, machine_name, command):
  """
  Sends a command from the host machine to a virtual machine.
  :param scenario_name: String with the scenario name
  :param machine_name: Machine's name
  :param command: Vagrant command to be executed
  :return: Response object containing the status of the request
  """
  return jsonify(vagrant_manager.vagrantMachineCommand(scenario_name, machine_name, command))

@celery.task(bind = True)
def getTaskStatus(self, task_id):
    """
    Gets Celery task's status.
    :param self: Celery object
    :param task_id: Task's id to be requested
    :return: Response object containing the status of the request
    """
    return self.AsyncResult(task_id)


@application.route('/vagrant/taskStatus/<task_id>')
def taskstatus(task_id):
    """
    Requests the status of a Celery task.
    :param task_id: Task's id to be requested.
    :return: Response object containing the status of the request
    """
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