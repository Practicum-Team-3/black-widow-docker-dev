import json
from unique_id import get_unique_id
from datetime import datetime
from Entities.Exploit import Exploit
from Entities.Vulnerability import Vulnerability
from Entities.VirtualMachine import VirtualMachine
from Entities.Entity import Entity


class Scenario(Entity):

    def __init__(self, scenario_name):
        # Variables
        self.scenario_name = scenario_name
        self.scenario_id = get_unique_id(length=8)
        now = datetime.now()
        self.creation_date = now.strftime("%d/%m/%Y %H:%M:%S")
        self.last_accessed = self.creation_date[:]
        self.description = ""
        self.exploit = Exploit()
        self.vulnerability = Vulnerability()
        self.machines = dict()

    def setExploit(self, exploit):
        """
        Sets the exploit info for this scenario
        :param exploit_info: Object which carries the exploit info
        """
        self.exploit = exploit

    def setVulnerability(self, vulnerability):
        """
        Sets the vulnerability info for this scenario
        :param vulnerability_info: Object which carries the vulnerability info
        """
        self.vulnerability = vulnerability

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
        scenario_dict["description"] = self.description
        scenario_dict["exploit"] = self.exploit.dictionary()
        scenario_dict["vulnerability"] = self.vulnerability.dictionary()
        scenario_dict["machines"] = dict()
        for name in self.machines:
            scenario_dict["machines"][name] = self.machines[name].dictionary()
        return scenario_dict

    def objectFromDictionary(self, dict):
        self.scenario_id = dict["scenario_id"]
        self.creation_date = dict["creation_date"]
        self.last_accessed = dict["last_accessed"]
        self.description = dict["description"]
        self.exploit = Exploit().objectFromDictionary(dict["exploit"])
        self.vulnerability = Vulnerability().objectFromDictionary(dict["vulnerability"])
        for m in dict["machines"]:
            self.machines[m] = VirtualMachine().objectFromDictionary(dict["machines"][m])
        return self