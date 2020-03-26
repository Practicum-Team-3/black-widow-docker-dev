import os
import subprocess
import re
from Managers.FileManager import FileManager
from Managers.ScenarioManager import ScenarioManager
from Entities.VagrantFile import VagrantFile

class VagrantManager(object):

    def __init__(self):
        self.file_manager = FileManager()
        self.vagrant_file = VagrantFile()
        self.scenario_manager = ScenarioManager()

    def createVagrantFiles(self, scenario_name):
        """
        Creates a vagrant file per machine in a scenario
        :param scenario_json: String with the scenario name
        :return: True if vagrant files were successfully created
        """
        self.file_manager.createMachineFolders(scenario_name)
        scenario_json = self.scenario_manager.getScenario(scenario_name)
        for machine_name in scenario_json["machines"]:
            machine = scenario_json["machines"][machine_name]
            machine_path = self.file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
            print(self.vagrant_file.vagrantFilePerMachine(machine , machine_path))
        result = {"result": True}
        return result

    def runVagrantUp(self, scenario_name):
        """
        Executes the vagrant up command for each machine in the scenario
        :param scenario_name: String with the scenario name
        :return: True if the vagrant up commands were successfully executed
        """
        self.createVagrantFiles(scenario_name)
        scenario_json = self.scenario_manager.getScenario(scenario_name)
        for machine_name in scenario_json["machines"]:
            machine_path = self.file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
            if not os.path.exists(machine_path):  # Proceed if path exists
                return
            os.chdir(machine_path)
            process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE,
                                       universal_newlines=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
        result = {"result": True}
        return result


    def sendCommand(self, scenario_name, machine_name, command, default_timeout = 5, show_output = True):
        #First we need to move to the directory of the given machine
        machine_path = self.file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
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

        if self.scenario_manager.scenarioExists(scenario_name):
            scenario_data = self.scenario_manager.getScenario(scenario_name)

            try:
                machines = scenario_data['machines']
                machine_to_ping = machines[destination_machine_name]
                machine_to_ping_network_settings = machine_to_ping['network_settings']
                destination_ip = machine_to_ping_network_settings['ip_address']
                ping_command = "ping -c {} {}".format(count, destination_ip)
                return_code = self.sendCommand(scenario_name, machine_name, ping_command)
                if return_code == 0:
                    print("Ping Succesful")
                    return True
                elif return_code == 1:
                    print("No answer from %s" % destination_machine_name)
                    return False
                else:
                    print("Another error as ocurred")
                    return False
            except KeyError:
                print("Machines not defined for this Scenario")
                return False
        else:
            print("Scenario %s not found" % scenario_name)
            return False


    def getAvailableBoxes(self):
        """
        Gets the available boxes in the Vagrant context
        :return: A list of string with the available boxes
        """
        # Variables
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
        return boxes