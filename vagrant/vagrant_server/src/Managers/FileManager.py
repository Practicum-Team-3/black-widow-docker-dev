import sys
import os
from pathlib import Path
import shutil
from Entities.Response import Response
from Entities.VagrantFile import VagrantFile
from Managers.SaltManager import SaltManager

class FileManager(object):
    def __init__(self):
        # Paths
        self.current_path = Path.cwd()
        self.scenarios_path = self.current_path /"scenarios"
        self.exploits_path = self.current_path / "exploits"
        self.vulnerabilities_path = self.current_path / "vulnerabilities"
        self.vagrant_file = VagrantFile()
        self.salt_manager = SaltManager()

    def getCurrentPath(self):
        """
        Gets the project folder path
        :return: String with the project path
        """
        return self.current_path

    def getScenariosPath(self):
        """
        Gets the scenarios folder path
        :return: String with the scenarios project path
        """
        return self.scenarios_path

    def getExploitsPath(self):
        """
        Gets the exploits folder path
        :return: String with the exploit project path
        """
        return self.exploits_path

    def getScenarioJSONPath(self, scenario_name):
        return self.scenarios_path / scenario_name / "JSON"

    def getExploitJSONPath(self, exploit_name):
        return self.exploits_path / exploit_name

    def getVulnerabilityJSONPath(self, vulnerability_name):
        return self.vulnerabilities_path / vulnerability_name

    def createScenarioFolders(self, scenario_json):
        """
        Creates a scenario folder with the JSON, Exploit, Vulnerability and Machines subfolders
        :param scenario_json: String with the scenario name
        :return: True if the scenario is created successfully
        """
        # Variables
        folders = ["Machines"]
        scenario_name = scenario_json['scenario_name']
        scenario_path = self.getScenariosPath() / scenario_name
        try:
            os.makedirs(scenario_path)
            for f in folders:
                path = scenario_path / f
                try:
                    os.makedirs(path)
                except OSError:
                    print("Creation of the directory %s failed" % path)
                except FileExistsError:
                    print("Directory ", path, " already exists")
                else:
                    print("Successfully created the directory %s" % path)
        except OSError:
            print("Creation of the directory %s failed" % scenario_path)
        except FileExistsError:
            print("Directory ", scenario_path," already exists")
        else:
            print("Successfully created the directory %s" % scenario_path)
        return

    def deleteScenariosFolder(self, scenario_name):
        scenario_path = self.getScenariosPath() / scenario_name
        try:
            shutil.rmtree(scenario_path)
        except OSError as e:
            print("Error: %s : %s" % (scenario_path, e.strerror))
        return

    def createMachineFolders(self, scenario_json):
        """
        Creates a folder for each machine in the scenario
        :param scenario_json: String with the scenario name
        :return: True if machine folders are created successfully
        """
        # Response message for the requester
        response = Response()
        try:
            machines = scenario_json['machines']
            scenario_name = scenario_json['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                machine_path = machines_path / machine_name
                machine = scenario_json["machines"][machine_name]
                if os.path.isdir(machine_path):
                    print("Folder already exists")
                else:
                    os.makedirs(machine_path)
                shared_folder = machine["shared_folders"][0]
                shared_folder_path = machine_path / shared_folder
                if os.path.isdir(shared_folder_path):
                    print("Shared folder already exists")
                else:
                    os.makedirs(shared_folder_path)

        except KeyError as key_not_found:
            print("%s has not been defined" % key_not_found)
            response.setResponse(False)
            response.setReason(key_not_found, " has not been defined")
        except OSError:
            print("OS Error")
            response.setResponse(False)
            response.setReason("OS Error")
        except:
            print("Unexpected error:", sys.exc_info()[0])
        response.setResponse(True)
        return response.dictionary()

    def createSaltStackFolder(self, scenario_json):
        """
        Creates a folder for each machine in the scenario
        :param scenario_json: String with the scenario name
        :return: True if machine folders are created successfully
        """
        # Response message for the requester
        response = Response()
        try:
            machines = scenario_json['machines']
            scenario_name = scenario_json['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                saltstack_path = machines_path / machine_name / 'saltstack'
                keys_path = machines_path / machine_name / 'saltstack' / 'keys'
                etc_path = machines_path / machine_name / 'saltstack' / 'conf'
                paths = [saltstack_path, keys_path, etc_path]
                for path in paths:
                    if os.path.isdir(path):
                        print("Folder already exists: ", path)
                    else:
                        os.makedirs(path)
        except KeyError as key_not_found:
            print("%s has not been defined" % key_not_found)
            response.setResponse(False)
            response.setReason(key_not_found, " has not been defined")
        except OSError:
            print("OS Error")
            response.setResponse(False)
            response.setReason("OS Error")
        except:
            print("Unexpected error:", sys.exc_info()[0])
        response.setResponse(True)
        return response.dictionary()

    def createSharedFolders(self, scenario_json):
        response = Response()
        try:
            machines = scenario_json['machines']
            scenario_name = scenario_json['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                shared_folder_path = machines_path / machine_name / "host_shared_folder"
                if os.path.isdir(shared_folder_path):
                    print("Folder already exists: ", shared_folder_path)
                else:
                    os.makedirs(shared_folder_path)
        except KeyError as key_not_found:
            print("%s has not been defined" % key_not_found)
            response.setResponse(False)
            response.setReason(key_not_found, " has not been defined")
        except OSError:
            print("OS Error")
            response.setResponse(False)
            response.setReason("OS Error")
        except:
            print("Unexpected error:", sys.exc_info()[0])
        response.setResponse(True)
        return response.dictionary()

    def createVagrantFiles(self, scenario_json):
        response = Response()
        for machine_name in scenario_json["machines"]:
            #Names
            scenario_name = scenario_json['scenario_name']
            minion_id = self.salt_manager.generateMinionID(scenario_name, machine_name)
            #Paths
            machine_path = self.getScenariosPath() / scenario_name / "Machines" / machine_name
            #Machine JSON
            machine = scenario_json["machines"][machine_name]
            #Generate vagrant files
            print('Vagrant file created: ', self.vagrant_file.generateVagrantFile(machine, machine_path, minion_id))
        response.setResponse(True)
        return response.dictionary()

    def createSaltFiles(self, scenario_json):
        response = Response()
        for machine_name in scenario_json["machines"]:
            # Names
            scenario_name = scenario_json['scenario_name']
            minion_id = self.salt_manager.generateMinionID(scenario_name, machine_name)
            #Paths
            machine_path = self.getScenariosPath() / scenario_name / "Machines" / machine_name
            keys_path = machine_path / 'saltstack' / 'keys'
            conf_path = machine_path / 'saltstack' / 'conf'
            #Generate salt files
            self.salt_manager.generateKeys(keys_path, minion_id)
            print('Minion config file created: ', self.salt_manager.generateMinionConfigFile(conf_path, minion_id))
        response.setResponse(True)
        return response.dictionary()
