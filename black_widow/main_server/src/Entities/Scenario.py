import json
from unique_id import get_unique_id
from datetime import datetime
from Entities.ExploitInfo import ExploitInfo
from Entities.VulnerabilityInfo import VulnerabilityInfo
from Managers.FileManager import FileManager

class Scenario(object):

    def __init__(self, scenario_name):
        self.file_manager = FileManager()
        #Variables
        self.scenario_name =  scenario_name
        self.scenario_id =  get_unique_id(length=8)
        now = datetime.now()
        self.creation_date = now.strftime("%d/%m/%Y %H:%M:%S")
        self.last_accessed = self.creation_date[:]
        self.exploit_info = ExploitInfo("" , "" , "")
        self.vulnerability_info = VulnerabilityInfo("" , "" , "" , "")
        self.machines = dict()

    def setExploitInfo(self , exploit_info):
        """
        Sets the exploit info for this scenario
        :param exploit_info: Object which carries the exploit info
        """
        self.exploit_info = exploit_info
    
    def setVulnerabilityInfo(self , vulnerability_info):
        """
        Sets the vulnerability info for this scenario
        :param vulnerability_info: Object which carries the vulnerability info
        """
        self.vulnerability_info = vulnerability_info
        
    def addVM(self, vm):
        """
        Adds a new virtual machine to this scenario
        :param vm: Object which carries the virtual machine data
        """
        self.machines[vm.name] = vm

    def dictionary(self):
        """
        Generates a dictionary for the Scenario object
        :return: A dictionary with Scenario data
        """
        scenario_dict = dict()
        scenario_dict["scenario_name"] = self.scenario_name
        scenario_dict["scenario_id"] = self.scenario_id
        scenario_dict["creation_date"] = self.creation_date
        scenario_dict["last_accessed"] = self.last_accessed
        scenario_dict["exploit_info"] = self.exploit_info.dictionary() if self.exploit_info else dict()
        scenario_dict["vulnerability_info"] = self.vulnerability_info.dictionary() if self.vulnerability_info else dict()
        scenario_dict["machines"] = dict()
        for name in self.machines:
          scenario_dict["machines"][name] = self.machines[name].dictionary()
        return scenario_dict
    
    def generateScenario(self, scenario_name):
        """
        Generates a scenario JSON file
        :param scenario_name: String with the scenario name
        :return: JSON file containing all the scenario data
        """
        json_dict = self.dictionary()
        json_name = self.scenario_name + ".json"
        with open(self.file_manager.getScenariosPath() / scenario_name / "JSON" / json_name, 'w') as outfile:
          json.dump(json_dict, outfile)
        json_string = json.dumps(json_dict , indent = 2)
        print(json_string)
        return json_string
  