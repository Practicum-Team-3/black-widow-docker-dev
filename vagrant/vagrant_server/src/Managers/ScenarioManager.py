import os
import json
from Managers.FileManager import FileManager
from Entities.Scenario import Scenario

class ScenarioManager(object):

    def __init__(self):
        self.file_manager = FileManager()

    def createScenario(self, scenario_name):
        """
        Creates a new scenario which includes the folders and the scenario JSON file
        :param scenario_name: String with the scenario name
        :return: True if the new scenario was successfully created
        """
        #Folder creation moved to FileManager
        self.file_manager.createScenarioFolders(scenario_name)
        scenario = Scenario(scenario_name)
        scenario.generateScenario(scenario_name)
        result = {"result": True}
        return result

    def getScenarios(self):
        """
        Gets the available scenarios
        :return: A list of strings with the available scenarios
        """
        # Variables
        scenarios = os.listdir(self.file_manager.getScenariosPath())
        scenarios_dict = {"scenarios": scenarios}
        return scenarios_dict

    def scenarioExists(self, scenario_name):
        """
        Check if a scenario exists
        :param scenario_name: String with the scenario name
        :return: False if the scenario JSON file does not exist and the path to the JSON file if it exist
        """
        scenario_dir_path = self.file_manager.getScenariosPath() / scenario_name / "JSON"
        if not os.path.isdir(scenario_dir_path):
            print("Scenario %s directory not found" % scenario_name)
            return False
        else:
            scenario_json_path = scenario_dir_path /  ''.join([scenario_name, ".json"])
            if not os.path.exists(scenario_json_path):
                print("Scenario %s json not found" % scenario_name)
                return None
            else:
                return scenario_json_path

    def getScenario(self, scenario_name):
        """
        Gets the scenario as a JSON file
        :param scenario_name: String with the scenario name
        :return: JSON file with the scenario info
        """
        scenario_json_path = self.scenarioExists(scenario_name)
        if scenario_json_path:
            try:
                with open(scenario_json_path) as json_file:
                    scenario_json = json.load(json_file)
                    return scenario_json
            except:
                print("Something went wrong while retrieving Scenario JSON")

    def editScenario(self, scenario_json):
        """
        Edits a current scenario with a JSON file
        :param scenario_name: String with the scenario name
        :param scenario_json: JSON file with the new scenario
        :return: True if the scenario has been successfully edited, otherwise False
        """
        scenario_name = scenario_json["scenario_name"]
        scenario_json_path = self.scenarioExists(scenario_name)
        if scenario_json_path:
            with open(scenario_json_path, 'w+') as outfile:
                outfile.write(json.dumps(scenario_json, indent=2))
                outfile.close()
            #THIS IS A PLACEHOLDER
            #It will try to create the folders every time the scenario is edited
            #new_scenario_dict = json.loads(new_scenario)
            return True
        else:
            return False

