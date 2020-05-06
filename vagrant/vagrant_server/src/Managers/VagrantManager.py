import os
import subprocess
import re
import psutil
import time
from CeleryApp import celery
from math import ceil
from Managers.FileManager import FileManager
from Managers.DatabaseManager import DatabaseManager
from Managers.SaltManager import SaltManager
from Entities.Response import Response

file_manager = FileManager()
db_manager = DatabaseManager()
salt_manager = SaltManager()

class VagrantManager():

    def getSystemInfo(self): 
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count = psutil.cpu_count(logical=False)
        memory = psutil.virtual_memory()
        mem = getattr(memory, 'total')
        memory_bytes = int(mem)
        gigabytes = float(1024 ** 3)
        total_ram = ceil(memory_bytes/gigabytes)
        info = {'cpu_count_logical' : cpu_count, 'cpu_count' : cpu_count, 'total_ram' : total_ram }
        response = Response()
        response.setResponse(True)
        response.setBody(info)
        return response.dictionary()


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
        process = subprocess.Popen(['vagrant', 'box', 'add', box_name, '--provider', 'virtualbox'], stdout=subprocess.PIPE,
                                   universal_newlines=True)

        message = "Downloading %s box..." % box_name
        self.update_state(state='PROGRESS',
                          meta={'current': 0, 'total': 100,
                                'message': message})
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                line = output.strip()
                print(line)
                progress = re.findall(r'\b(?<!\.)(?!0+(?:\.0+)?%)(?:\d|[1-9]\d|100)(?:(?<!100)\.\d+)?%', line)
                if progress:
                    number = progress[0]
                    number = number.replace("%", "")
                    current = int(number)
                    self.update_state(state='PROGRESS',
                          meta={'current': current, 'total': 100,
                                'message': message})
        message = "Download Complete"
        print(message)
        return {'current': 100, 'total': 100, 'message': message,
            'result': message}

    @celery.task(name='VagrantManager.removeBoxByName', bind=True)
    def removeBoxByName(self, box_name):

        message = "Removing %s box..." % box_name
        self.update_state(state='PROGRESS',
                          meta={'current': 0, 'total': 100,
                                'message': message})

        process = subprocess.Popen(['vagrant', 'box', 'remove', box_name], stdout=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        message = "Box removed."
        return {'current': 100, 'total': 100, 'message': message,
            'result': message}

    @celery.task(name='VagrantManager.addBoxByOVAFile', bind=True)
    def addBoxByOVAFile(self, file_name):
        ova_file = "".join([file_name, ".ova"])
        box_file = "".join([file_name, ".box"])

        print("Hello Folks")
        print(ova_file)
        VagrantManager._runCommandFromShell(['pwd'])
        # IMPORTING OVA FILE INTO VIRTUAL BOX
        print('IMPORTING OVA FILE INTO VIRTUAL BOX')
        VagrantManager._runCommandFromShell(['vboxmanage', 'import', ova_file])

        # GETTING VIRTUAL MACHINE ID
        print('GETTING VIRTUAL MACHINE ID')
        process = subprocess.Popen(['vboxmanage', 'list', 'vms'], stdout=subprocess.PIPE,
                                   universal_newlines=True)
        box_id = ""
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
            if file_name in output:
                box_id = output
        pattern = '(^.*{)(.+)(}.*)'
        match = re.search(pattern, box_id)
        box_id = match.group(2)
        print('Box id = ', box_id)

        # PACKAGING VIRTUAL MACHINE INTO A BOX
        print('PACKAGING VIRTUAL MACHINE INTO A BOX')
        VagrantManager._runCommandFromShell(['vagrant', 'package', '--base', box_id, '--output', box_file])

        # ADDING BOX BY NAME
        # vagrant add box cumulus.box --name cumulus
        print('ADDING BOX TO VAGRANT')
        VagrantManager._runCommandFromShell(['vagrant', 'box', 'add', box_file, '--name', file_name])

        message = "Box added using OVA file."
        return {'current': 100, 'total': 100, 'message': message, 'result': message}

    @staticmethod
    def vagrantStatus(machine_name, machine_path):
        """
        Determines the status of the given vm
        :param machine_name: String with the machine name
        :param machine_path: Path to the given machine
        :return: String representing the status of the machine, False if machine not present
        """
        os.chdir(machine_path)
        process = subprocess.Popen(['vagrant', 'status'], stdout=subprocess.PIPE,
                                           universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                line = output.strip()
                if machine_name in line:
                    line = line.split()
                    if len(line) > 0:
                        return line[1]
        return False

    def vagrantMachineCommand(self, scenario_name, machine_name, command):
        """
        Runs the given vagrant command on the desired machine, if allowed. 
        :param scenario_name: Name of scenario containing the machine
        :param machine_name: String with the machine name
        :return: Response object containing the status of the machine after execution of command
        """
        response = Response()
        scenario = db_manager.getScenario(scenario_name)
        if scenario:
            scenario_json = scenario[0]
            machine_uuid = scenario_json["machines"][machine_name]["uuid"]

            allowed_commands = ['suspend','halt','resume','status']
            if command not in allowed_commands:
                response = Response(False, "Given command not allowed")
                return response.dictionary()

            else:
                try:
                    machine_path = file_manager.getScenariosPath() / scenario_name / "Machines" / machine_uuid
                    if command != 'status':
                        os.chdir(machine_path)
                        subprocess.run(['vagrant', command])
                    machine_state = VagrantManager.vagrantStatus(machine_uuid, machine_path)
                    response = Response(True, body={machine_name: machine_state})
                    return response.dictionary()
                except OSError:
                    error_message = "OS ERROR while running %s command on %s machine " % command, machine_name
                    print(error_message)
                    response = Response(False, error_message)
                    return response.dictionary()
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
        message = ""
        scenario = db_manager.getScenario(scenario_name)
        safe_from_purge = list()

        if scenario:
            scenario_json = scenario[0]
            VagrantManager._createFoldersAndFiles(scenario_json)
            completed = 0 #number of VMs started
            total = len(scenario_json["machines"]) #Number of machines in scenario
            message = "Starting all VMs inside %s scenario" % scenario_name
            self.update_state(state='PROGRESS',
                          meta={'current': completed, 'total': total,
                                'message': message})

            for machine_name in scenario_json["machines"]:
                # Names
                machine_uuid = scenario_json["machines"][machine_name]["uuid"]
                safe_from_purge.append(machine_uuid)
                scenario_name = scenario_json['scenario_name']
                #Paths
                machine_path = file_manager.getScenariosPath() / scenario_name / "Machines" / machine_uuid
                os.chdir(machine_path)
                process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE,
                                           universal_newlines=True)
                message = "Working on %s" % machine_name
                self.update_state(state='PROGRESS',
                          meta={'current': completed, 'total': total,
                                'message': message})
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                        message = output.strip()
                        self.update_state(state='PROGRESS',
                          meta={'current': completed, 'total': total,
                                'message': message})
                #Accepting public keys for this virtual machine aka minion
                salt_manager.acceptKeys(machine_uuid)
                time.sleep(3)
                #Ping minion id
                salt_manager.testPing(machine_uuid)
                #Run beats salt formulas
                salt_manager.runSaltHighstate(machine_uuid)
                #Copying beats config files
                salt_manager.copyingBeatsConfigFiles(machine_uuid)
                completed += 1 #For progress bar
            message = "Completed Vagrant Up"
            self.update_state(state='PROGRESS',
                          meta={'current': completed, 'total': total,
                                'message': message})
        else:
            message = "Scenario does not exist"

        machines_running = {}
        for machine_name in scenario_json["machines"]:
            machine_uuid = scenario_json["machines"][machine_name]["uuid"]
            machine_path = file_manager.getScenariosPath() / scenario_name / "Machines" / machine_uuid
            machine_name = scenario_name + "_" + machine_name
            machines_running[machine_name] = VagrantManager.vagrantStatus(machine_name, machine_path)
               

        self.update_state(state='COMPLETE',
                          meta={'current': completed, 'total': total,
                                'message': message})


        VagrantManager._purgeMachines(scenario_name, safe_from_purge)        
        return {'current': total, 'total': total, 'message': message,
            'result': machines_running}

    @staticmethod
    def _createFoldersAndFiles(scenario_json):
        """
        Creates a vagrant file per machine in a scenario
        :param scenario_json: String with the scenario name
        :return: True if vagrant files were successfully created
        """
        #Folders creation
        VagrantManager._createFolders(scenario_json)
        #Files creation
        VagrantManager._createFiles(scenario_json)
        return

    @staticmethod
    def _createFolders(scenario_json):
        file_manager.createScenarioFolders(scenario_json)
        file_manager.createMachineFolders(scenario_json)
        file_manager.createSharedFolders(scenario_json)
        file_manager.createSaltStackFolder(scenario_json)
        return

    @staticmethod
    def _createFiles(scenario_json):
        file_manager.createVagrantFiles(scenario_json)
        file_manager.createSaltFiles(scenario_json)
        return
    
    @staticmethod
    def _purgeMachines(scenario_name, safe_machines):
        file_manager.purgeMachines(scenario_name, safe_machines)
        return

    def sendCommand(self, scenario_name, machine_name, command, default_timeout = 5, show_output = True):
        response = Response()
        scenario = db_manager.getScenario(scenario_name)
        return_code = ''
        if scenario:
            scenario_json = scenario[0]
            #First we need to move to the directory of the given machine
            machine_uuid = scenario_json["machines"][machine_name]["uuid"]
            machine_path = file_manager.getScenariosPath() / scenario_name / "Machines" / machine_uuid
            #using "vagrant ssh -c 'command' <machine>" will only try to execute that command and return, CHANGE THIS
            connect_command = "vagrant ssh -c '{}' {}".format(command, machine_uuid)
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
        else:
            response.setResponse(False)
            response.setReason('Scenario doesn\'t exist')
        return return_code

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

    @staticmethod
    def _runCommandFromShell(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        return
