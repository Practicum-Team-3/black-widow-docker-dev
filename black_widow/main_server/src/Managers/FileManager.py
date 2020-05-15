import sys
import os
from pathlib import Path
from Entities.Response import Response

class FileManager(object):
    def __init__(self):
        # Paths
        self.current_path = Path.cwd()
        self.scenarios_path = self.current_path /"scenarios"
        self.exploits_path = self.current_path / "exploits"
        self.vulnerabilities_path = self.current_path / "vulnerabilities"

    def getCurrentPath(self):
        """
        test
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
        """
        Gets scenario JSON path inside a machine.
        :param scenario_name: Scenario name string
        :return: JSON path folder
        """
        return self.scenarios_path / scenario_name / "JSON"

    def getExploitJSONPath(self, exploit_name):
        """
        Gets exploit JSON path.
        :param exploit_name: Exploit name to search
        :return: Exploit path
        """
        return self.exploits_path / exploit_name

    def getVulnerabilityJSONPath(self, vulnerability_name):
        """
        Gets vulnerability JSON path.
        :param vulnerability_name: Vulnerability name to search
        :return: Vulnerability path
        """
        return self.vulnerabilities_path / vulnerability_name

    def createScenarioFolders(self, scenario_json):
        """
        Creates a scenario folder with the JSON, Exploit, Vulnerability and Machines subfolders
        :param scenario_json: String with the scenario name
        :return: True if the scenario is created successfully
        """
        self.console_manager.printRed('Creating scenario folders: ')
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
                    self.console_manager.printGreen(''.join(["Creation of the directory ", str(path), " failed."]))
                except FileExistsError:
                    self.console_manager.printGreen(''.join(["Directory ", str(path), " already exists"]))
                else:
                    self.console_manager.printGreen(''.join(["Successfully created the directory ", str(path)]))
        except OSError:
            self.console_manager.printGreen(''.join(["Creation of the directory ", str(scenario_path), " failed."]))
        except FileExistsError:
            self.console_manager.printGreen(''.join(["Directory ", str(scenario_path), " already exists"]))
        else:
            self.console_manager.printGreen(''.join(["Successfully created the directory ", str(scenario_path)]))
        return

    def purgeMachines(self, scenario_name, safe_machines):
        """
        Deletes machines that no longer exist within the scenario.
        :param scenario_name: Scenario name as a string
        :param safe_machines: Collection containing machines that must remain within the scenario
        :return: None
        """
        also_safe = ["VagrantFile", "host_shared_folder", "salt"]
        safe_machines.append(also_safe)
        path = self.getScenariosPath() / scenario_name / "Machines"
        list_subfolders = os.listdir(path)
        for folder in list_subfolders:
            if folder not in safe_machines:
                try:
                    to_delete = path + "/"+ folder
                    shutil.rmtree(to_delete)
                except OSError as e:
                    print("Error: %s : %s" % (folder, e.strerror))
        return

    def deleteScenariosFolder(self, scenario_name):
        """
        Deletes not used scenario folders.
        :param scenario_name: Scenario name as a string
        :return: None
        """
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
        self.console_manager.printRed('Creating machine folders: ')
        try:
            machines = scenario_json['machines']
            scenario_name = scenario_json['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                machine_uuid = scenario_json["machines"][machine_name]["uuid"]
                machine_path = machines_path / machine_uuid
                if os.path.isdir(machine_path):
                    self.console_manager.printGreen("Folder already exists")
                else:
                    os.makedirs(machine_path)
        except KeyError as key_not_found:
            self.console_manager.printGreen(''.join([key_not_found, " has not been defined"]))
            response.setResponse(False)
            response.setReason(key_not_found, " has not been defined")
        except OSError:
            self.console_manager.printGreen("OS Error")
            response.setResponse(False)
            response.setReason("OS Error")
        except:
            self.console_manager.printGreen(''.join(["Unexpected error:", sys.exc_info()[0]]))
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
        self.console_manager.printRed('Creating saltstack folders: ')
        try:
            machines = scenario_json['machines']
            scenario_name = scenario_json['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                machine_uuid = scenario_json["machines"][machine_name]["uuid"]
                saltstack_path = machines_path / machine_uuid / 'salt'
                keys_path = saltstack_path / 'keys'
                etc_path = saltstack_path / 'conf'
                paths = [saltstack_path, keys_path, etc_path]
                for path in paths:
                    if os.path.isdir(path):
                        self.console_manager.printGreen("Folder already exists")
                    else:
                        os.makedirs(path)
        except KeyError as key_not_found:
            self.console_manager.printGreen(''.join([key_not_found, " has not been defined"]))
            response.setResponse(False)
            response.setReason(key_not_found, " has not been defined")
        except OSError:
            self.console_manager.printGreen("OS Error")
            response.setResponse(False)
            response.setReason("OS Error")
        except:
            self.console_manager.printGreen(''.join(["Unexpected error:", sys.exc_info()[0]]))
        response.setResponse(True)
        return response.dictionary()

    def createSharedFolders(self, scenario_json):
        """
        Creates the shared folder within a scenario.
        :param scenario_json: JSON containing the scenario data
        :return: Response object containing request info
        """
        response = Response()
        self.console_manager.printRed('Creating shared folders: ')
        try:
            machines = scenario_json['machines']
            scenario_name = scenario_json['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                machine_uuid = scenario_json["machines"][machine_name]["uuid"]
                shared_folder_path = machines_path / machine_uuid / "host_shared_folder"
                if os.path.isdir(shared_folder_path):
                    self.console_manager.printGreen("Folder already exists")
                else:
                    os.makedirs(shared_folder_path)
        except KeyError as key_not_found:
            self.console_manager.printGreen(''.join([key_not_found, " has not been defined"]))
            response.setResponse(False)
            response.setReason(key_not_found, " has not been defined")
        except OSError:
            self.console_manager.printGreen("OS Error")
            response.setResponse(False)
            response.setReason("OS Error")
        except:
            self.console_manager.printGreen(''.join(["Unexpected error:", sys.exc_info()[0]]))
        response.setResponse(True)
        return response.dictionary()

    def createVagrantFiles(self, scenario_json):
        """
        Creates a vagrant file per machine in a scenario.
        :param scenario_json: JSON containing the scenario data
        :return: Response object containing request info
        """
        response = Response()
        self.console_manager.printRed('Creating vagrant file')
        for machine_name in scenario_json["machines"]:
            #Names
            scenario_name = scenario_json['scenario_name']
            machine_uuid = scenario_json["machines"][machine_name]["uuid"]
            #Paths
            machine_path = self.getScenariosPath() / scenario_name / "Machines" / machine_uuid
            #Machine JSON
            machine = scenario_json["machines"][machine_name]
            #Generate vagrant files
            self.console_manager.printBlue(self.vagrant_file.generateVagrantFile(machine, machine_path, machine_uuid))
        response.setResponse(True)
        return response.dictionary()

    def createSaltFiles(self, scenario_json):
        """
        Creates the salt files per each machine in a scenario.
        :param scenario_json: JSON containing the scenario data
        :return: Response object containing request info
        """
        response = Response()
        self.console_manager.printRed('Creating saltstack files')
        for machine_name in scenario_json["machines"]:
            # Names
            scenario_name = scenario_json['scenario_name']
            machine_uuid = scenario_json["machines"][machine_name]["uuid"]
            #Paths
            machine_path = self.getScenariosPath() / scenario_name / "Machines" / machine_uuid
            keys_path = machine_path / 'salt' / 'keys'
            conf_path = machine_path / 'salt' / 'conf'
            #Generate salt files
            self.salt_manager.generateKeys(keys_path, machine_uuid)
            self.console_manager.printBlue(self.salt_manager.generateMinionConfigFile(conf_path, machine_uuid))
        response.setResponse(True)
        return response.dictionary()