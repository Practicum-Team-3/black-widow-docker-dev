import os
import json
import uuid
from Managers.FileManager import FileManager
from Managers.DatabaseManager import DatabaseManager
from Entities.Scenario import Scenario
from Entities.Response import Response

class ScenarioManager():

    def __init__(self, db_manager = DatabaseManager()):
        self.file_manager = FileManager()
        self.db_manager = db_manager
        self.scenarios_dict = self._initializeFromDatabase()

    def _initializeFromDirectory(self):
        """
        Initializes the scenario's runtime objects using data from the host folders.
        :return: Dictionary containing scenario's data
        """
        # Variables
        scenarios_dict = dict()
        scenarios = os.listdir(self.file_manager.getScenariosPath())
        for scenario_name in scenarios:
            json_name = ''.join([scenario_name , ".json"])
            with open(self.file_manager.getScenarioJSONPath(scenario_name) / json_name) as outfile:
                scenario_dict = json.load(outfile)
            scenario = Scenario(scenario_name).objectFromDictionary(scenario_dict)
            scenarios_dict[scenario_name] = scenario
        return scenarios_dict

    def _initializeFromDatabase(self):
        """
        Pre-populates the database with scenarios.
        :return: Dictionary containing scenario's data
        """
        # Variables
        scenarios_dict = dict()
        scenarios = self.db_manager.getScenarios()
        for raw_scenario in scenarios:
            del raw_scenario["_id"]
            scenario_name = raw_scenario["scenario_name"]
            scenario = Scenario(scenario_name).objectFromDictionary(raw_scenario)
            scenarios_dict[scenario_name] = scenario
        return scenarios_dict

    def newEmpty(self, scenario_name):
        """
        Creates a new scenario which includes the folders and the scenario JSON file
        :param scenario_name: String with the scenario name
        :return: Response object containing the status of the request
        """
        #Folder creation moved to FileManager
        response = Response()
        if scenario_name not in self.scenarios_dict:
            #self.file_manager.createScenarioFolders(scenario_name)
            scenario = Scenario(scenario_name)
            self.scenarios_dict[scenario_name] = scenario
            #self._saveScenarioAsJSON(scenario)
            self.db_manager.insertScenario(scenario.dictionary().copy())
            response.setResponse(True)
            response.setBody(scenario.dictionary())
        else:
            response.setResponse(False)
            response.setReason('Scenario already exist')
            response.setBody(dict())

        return response.dictionary()

    def getAll(self):
        """
        Gets the available scenarios
        :return: Response object containing the status of the request
        """
        # Variables
        scenarios_dict = {"scenarios": [self.scenarios_dict[s].scenario_name for s in self.scenarios_dict]}
        response = Response()
        response.setResponse(True)
        response.setBody(scenarios_dict)
        return response.dictionary()


    def getOne(self, scenario_name):
        """
        Gets the scenario as a JSON file
        :param scenario_name: String with the scenario name
        :return: Response object containing the status of the request
        """
        response = Response()
        if scenario_name in self.scenarios_dict:
            response.setResponse(True)
            response.setBody(self.scenarios_dict[scenario_name].dictionary())
        else:
            response.setResponse(False)
            response.setReason('Scenario doesn\'t exist')
            response.setBody(dict())
        return response.dictionary()



    def editOne(self, scenario_json):
        """
        Edits a current scenario with a JSON file
        :param scenario_json: JSON file with the new scenario
        :return: Response object containing the status of the request
        """
        response = Response()
        print(scenario_json)
        scenario_name = scenario_json["scenario_name"]
        if scenario_name in self.scenarios_dict:

            if "machines" in scenario_json:
                for machine in scenario_json["machines"]:

                    if scenario_json["machines"][machine]["uuid"] == "":
                        new_uuid = uuid.uuid4()
                        new_uuid = str(new_uuid).replace('-', '')
                        print("Unique id: " , new_uuid)
                        scenario_json['machines'][machine]['uuid'] = new_uuid
            

            scenario_json = Scenario(scenario_name).objectFromDictionary(scenario_json)
            
            
            self.scenarios_dict[scenario_name] = scenario_json
            #self._saveScenarioAsJSON(new_scenario)
            self.db_manager.editScenario(scenario_json.dictionary().copy())
            response.setResponse(True)
            response.setBody(self.scenarios_dict[scenario_name].dictionary())
        else:
            response.setReason('Scenario doesn\'t exist')
            response.setResponse(False)

            response.setBody(dict())
        return response.dictionary()

    def deleteOne(self, scenario_name):
        """
        Deletes one scenario from the database.
        :param scenario_name: Scenario's name string
        :return: Response object containing the status of the request
        """
        response = Response()
        if scenario_name in self.scenarios_dict:
            deleted_scenario = self.scenarios_dict.pop(scenario_name)
            #self.file_manager.deleteScenariosFolder(scenario_name)
            self.db_manager.deleteScenario(scenario_name)
            response.setResponse(True)
            response.setBody(deleted_scenario.dictionary())
        else:
            response.setResponse(False)
            response.setReason('Scenario doesn\'t exist')
            response.setBody(dict())
        return response.dictionary()

    def scenarioExists(self, scenario_name):
        """
        Check if a scenario exists.
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

    def _saveScenarioAsJSON(self, scenario):
        """
        Saves a scenario as a JSON file
        :param scenario: Scenario's name string
        :return: None
        """
        scenario_json_path = self.file_manager.getScenarioJSONPath(scenario.scenario_name) / ''.join([scenario.scenario_name, ".json"])
        if scenario_json_path:
            with open(scenario_json_path, 'w+') as outfile:
                outfile.write(json.dumps(scenario.dictionary(), indent=2))
                outfile.close()
        return