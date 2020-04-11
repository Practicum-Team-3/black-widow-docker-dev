import os
import subprocess
import re
from CeleryApp import celery
from Managers.FileManager import FileManager
from Managers.DatabaseManager import DatabaseManager
from Entities.VagrantFile import VagrantFile
from Entities.Response import Response

file_manager = FileManager()
db_manager = DatabaseManager()
vagrant_file = VagrantFile()

class VagrantManager():

    def getAvailableBoxes(self):
        """
        Gets the available boxes in the Vagrant context
        :return: A list of string with the available boxes
        """
        # Variables
        response = Response()
        boxes = {}
        boxNum = 0
        boxlist = subprocess.check_output("vagrant box list", shell=True)
        boxlist = str(boxlist)
        boxlist = re.sub(r"(^[b']|'|\s(.*?)\\n)", " ", boxlist)
        boxlist = boxlist.split(" ")
        boxlist = filter(None, boxlist)

        print("Loading available Vanilla VMs")

        for boxName in boxlist:
            boxNum = boxNum + 1
            boxes[boxNum] = boxName
            print("[ " + str(boxNum) + " ]" + boxName)
        response.setResponse(True)
        response.setBody(boxes)
        return response.dictionary()

    @celery.task(name='VagrantManager.addBoxByName', bind=True)
    def addBoxByName(self, box_name):
        response = Response()
        process = subprocess.Popen(['vagrant', 'box', 'add', box_name], stdout=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        response.setResponse(True)
        response.setStatus(self.AsyncResult(self.request.id).state)
        response.setTaskID(self.request.id)
        return response.dictionary()

    @celery.task(name='VagrantManager.removeBoxByName', bind=True)
    def removeBoxByName(self, box_name):
        response = Response()
        process = subprocess.Popen(['vagrant', 'box', 'remove', box_name], stdout=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        response.setResponse(True)
        response.setStatus(self.AsyncResult(self.request.id).state)
        response.setTaskID(self.request.id)
        return response.dictionary()

    @staticmethod
    def createVagrantFiles(scenario_name):
        """
        Creates a vagrant file per machine in a scenario
        :param scenario_json: String with the scenario name
        :return: True if vagrant files were successfully created
        """
        response = Response()
        file_manager.createMachineFolders(scenario_name)
        scenario = db_manager.getScenario(scenario_name)
        if scenario:
            scenario_json = scenario[0]
            for machine_name in scenario_json["machines"]:
                machine = scenario_json["machines"][machine_name]
                machine_path = file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
                if scenario_json["machines"][machine_name]['shared_folders']:
                    shared_folder_name = scenario_json["machines"][machine_name]['shared_folders'][0][2:]
                    shared_folder_path = machine_path / shared_folder_name
                    file_manager.createSharedFolders(shared_folder_path)
                print('Vagrant File created: ', vagrant_file.vagrantFilePerMachine(machine, machine_path))
            response.setResponse(True)
        else:
            response.setResponse(False)
            response.setReason('Scenario doesn\'t exist')
        return response.dictionary()

    @celery.task(name='VagrantManager.runVagrantUp', bind=True)
    def runVagrantUp(self, scenario_name):
        """
        Executes the vagrant up command for each machine in the scenario
        :param scenario_name: String with the scenario name
        :return: True if the vagrant up commands were successfully executed
        """
        response = Response()
        VagrantManager.createVagrantFiles(scenario_name)
        scenario = db_manager.getScenario(scenario_name)
        if scenario:
            scenario_json = scenario[0]
            for machine_name in scenario_json["machines"]:
                machine_path = file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
                shared_folder_name = scenario_json["machines"][machine_name]['shared_folders'][0][2:]
                shared_folder_path = machine_path / shared_folder_name
                if not os.path.exists(machine_path):  # Proceed if path exists
                    response.setResponse(False)
                    response.setReason("Machine path doesn't exist")
                    break
                if not os.path.exists(shared_folder_path):  # Proceed if path exists
                    response.setResponse(False)
                    response.setReason("Shared folder path doesn't exist")
                    break
                os.chdir(machine_path)
                process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE,
                                           universal_newlines=True)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
            response.setResponse(True)
        else:
            response.setResponse(False)
            response.setReason('Scenario doesn\'t exist')
        response.setStatus(self.AsyncResult(self.request.id).state)
        response.setTaskID(self.request.id)
        return response.dictionary()


    def sendCommand(self, scenario_name, machine_name, command, default_timeout = 5, show_output = True):
        #First we need to move to the directory of the given machine
        machine_path = file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
        #using "vagrant ssh -c 'command' <machine>" will only try to execute that command and return, CHANGE THIS
        connect_command = "vagrant ssh -c '{}' {}".format(command, machine_name)
        sshProcess = subprocess.Popen(connect_command,
                                    cwd=machine_path,
                                    stdin=subprocess.PIPE, 
                                    stdout = subprocess.PIPE,
                                    universal_newlines=True,
                                    shell=True,
                                    bufsize=0)
        #wait for the execution to finish, process running on different shell
        sshProcess.wait()
        sshProcess.stdin.close()
        return_code = sshProcess.returncode

        if show_output:
            for line in sshProcess.stdout:
                if line == "END\n":
                    break
                print(line,end="")

            for line in sshProcess.stdout:
                if line == "END\n":
                    break
                print(line,end="")
        return return_code

    def restartVM(self, machine_name):
        pass

    def haltVM(self, machine_name):
        pass

    def testNetworkPing(self, scenario_name, machine_name, destination_machine_name, count=1):
        response = Response()
        scenario = db_manager.getOne(scenario_name)
        if scenario:
            scenario_data = scenario[0]
            try:
                machines = scenario_data['machines']
                machine_to_ping = machines[destination_machine_name]
                machine_to_ping_network_settings = machine_to_ping['network_settings']
                destination_ip = machine_to_ping_network_settings['ip_address']
                ping_command = "ping -c {} {}".format(count, destination_ip)
                return_code = self.sendCommand(scenario_name, machine_name, ping_command)
                if return_code == 0:
                    print("Ping Succesful")
                    response.setResponse(True)
                    response.setReason("Ping Succesful")
                elif return_code == 1:
                    print("No answer from %s" % destination_machine_name)
                    response.setResponse(False)
                    response.setReason("No answer from %s" % destination_machine_name)
                else:
                    print("Another error as ocurred")
                    response.setResponse(False)
                    response.setReason("Another error as ocurred")
            except KeyError:
                print("Machines not defined for this Scenario")
                response.setResponse(False)
                response.setReason("Machines not defined for this Scenario")
        else:
            print("Scenario %s not found" % scenario_name)
            response.setResponse(False)
            response.setReason("Scenario %s not found" % scenario_name)
        return response.dictionary()
