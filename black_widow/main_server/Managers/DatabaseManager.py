'''
  Run mongoDB server:
    - cd C:\Program Files\MongoDB\Server\4.2\bin
    - mongod

  Create database:
    - use soft_prac

  Create collections:
    - db.createCollection('scenarios')
'''

import pymongo
import os
from Managers.FileManager import FileManager
from Managers.ConfigManager import ConfigManager
from Entities.Scenario import Scenario
from Entities.Scenario import Exploit
from Entities.Vulnerability import Vulnerability
import json

class DatabaseManager():

    def __init__(self):
        self.file_manager = FileManager()
        self.url = ConfigManager().mongoURL()
        self.db_name = "soft_prac"
        self.scenarios_col_name = 'scenarios'
        self.exploits_col_name = 'exploits'
        self.vulnerabilities_col_name = 'vulnerabilities'
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[self.db_name]
        self.scenarios_col = self.db[self.scenarios_col_name]
        self.exploits_col = self.db[self.exploits_col_name]
        self.vulnerabilities_col = self.db[self.vulnerabilities_col_name]
        self.addScenariosToDB()
        self.addExploitsToDB()
        self.addVulnerabilitiesToDB()

    def _initializeScenariosFromDirectory(self):
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

    def addScenariosToDB(self):
        scenarios_to_add = ['Scenario_1', 'Scenario_3']
        currentScenarios = self.getScenarios()
        scenarios_list = [scenario['scenario_name'] for scenario in currentScenarios]
        scenarios_set = set(scenarios_list)
        for scenario_name in scenarios_to_add:
            if scenario_name not in scenarios_set:
                json_name = ''.join([scenario_name, ".json"])
                with open(self.file_manager.getScenarioJSONPath(scenario_name) / json_name) as outfile:
                    scenario_dict = json.load(outfile)
                scenario = Scenario(scenario_name).objectFromDictionary(scenario_dict)
                self.insertScenario(scenario.dictionary().copy())
        return

    def addExploitsToDB(self):
        exploits_to_add = ['Django_3_0_Cross-Site_Request_Forgery_Token_Bypass']
        currentExploits = self.getExploits()
        exploits_list = [exploit['name'] for exploit in currentExploits]
        exploits_set = set(exploits_list)
        for exploit_name in exploits_to_add:
            if exploit_name not in exploits_set:
                json_name = ''.join([exploit_name, ".json"])
                with open(self.file_manager.getExploitJSONPath(exploit_name) / json_name) as outfile:
                    exploit_dict = json.load(outfile)
                exploit = Exploit().objectFromDictionary(exploit_dict)
                self.insertExploit(exploit.dictionary().copy())
        return

    def addVulnerabilitiesToDB(self):
        vulnerabilities_to_add = ['rConfig_3_9_searchColumn_SQL_Injection']
        currentVulnerabilities = self.getVulnerabilities()
        vulnerabilities_list = [vulnerability['name'] for vulnerability in currentVulnerabilities]
        vulnerabilities_set = set(vulnerabilities_list)
        for vulnerability_name in vulnerabilities_to_add:
            if vulnerability_name not in vulnerabilities_set:
                json_name = ''.join([vulnerability_name, ".json"])
                with open(self.file_manager.getVulnerabilityJSONPath(vulnerability_name) / json_name) as outfile:
                    vulnerability_dict = json.load(outfile)
                vulnerability = Vulnerability().objectFromDictionary(vulnerability_dict)
                self.insertVulnerability(vulnerability.dictionary().copy())
        return

    #CRUD: CREATE, READ, UPDATE and DELETE

    #Scenarios
    def insertScenario(self, scenario_json):
        doc = self.scenarios_col.insert_one(scenario_json)
        return doc.inserted_id

    def getScenarioNames(self):
        return [doc['scenario_name'] for doc in self.scenarios_col.find()]

    def getScenarios(self):
        return [doc for doc in self.scenarios_col.find()]

    def getScenario(self, scenario_name):
        query = {'scenario_name': scenario_name}
        return [doc for doc in self.scenarios_col.find(query)]

    def editScenario(self, scenario_json):
        query = {'scenario_name': scenario_json['scenario_name']}
        new_doc = {"$set": scenario_json }
        doc = self.scenarios_col.update_one(query, new_doc)
        return doc.modified_count

    def deleteScenario(self, scenario_name):
        query = {'scenario_name': scenario_name}
        doc = self.scenarios_col.delete_one(query)
        return doc.deleted_count

    #Exploits
    def insertExploit(self, exploit_json):
        doc = self.exploits_col.insert_one(exploit_json)
        return doc.inserted_id

    def getExploitNames(self):
        return [doc['name'] for doc in self.exploits_col.find()]

    def getExploits(self):
        return [doc for doc in self.exploits_col.find()]

    def getExploit(self, exploit_name):
        query = {'name': exploit_name}
        return [doc for doc in self.exploits_col.find(query)]

    def editExploit(self, exploit_json):
        query = {'name': exploit_json['name']}
        new_doc = {"$set": exploit_json }
        doc = self.exploits_col.update_one(query, new_doc)
        return doc.modified_count

    def deleteExploit(self, exploit_name):
        query = {'name': exploit_name}
        doc = self.exploits_col.delete_one(query)
        return doc.deleted_count

    #Vulnerabilities
    def insertVulnerability(self, vulnerability_json):
        doc = self.vulnerabilities_col.insert_one(vulnerability_json)
        return doc.inserted_id

    def getVulnerabilityNames(self):
        return [doc['name'] for doc in self.vulnerabilities_col.find()]

    def getVulnerabilities(self):
        return [doc for doc in self.vulnerabilities_col.find()]

    def getVulnerability(self, vulnerability_name):
        query = {'name': vulnerability_name}
        return [doc for doc in self.vulnerabilities_col.find(query)]

    def editVulnerability(self, vulnerability_json):
        query = {'name': vulnerability_json['name']}
        new_doc = {"$set": vulnerability_json }
        doc = self.vulnerabilities_col.update_one(query, new_doc)
        return doc.modified_count

    def deleteVulnerability(self, vulnerability_name):
        query = {'name': vulnerability_name}
        doc = self.vulnerabilities_col.delete_one(query)
        return doc.deleted_count