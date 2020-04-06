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
from Entities.Scenario import Scenario
import json

class DatabaseManager():

    def __init__(self, url=""):
        self.file_manager = FileManager()
        self.url = url
        self.db_name = "soft_prac"
        self.scenarios_col_name = 'scenarios'
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[self.db_name]
        self.scenarios_col = self.db[self.scenarios_col_name]
        self.prePopulateDB()

    def _initializeScenariosFromDirectory(self):
        # Variables
        scenarios_dict = dict()
        scenarios = os.listdir(self.file_manager.getScenariosPath())
        for scenario_name in scenarios:
            json_name = ''.join([scenario_name , ".json"])
            with open(self.file_manager.getJSONPath(scenario_name) / json_name) as outfile:
                scenario_dict = json.load(outfile)
            scenario = Scenario(scenario_name).objectFromDictionary(scenario_dict)
            scenarios_dict[scenario_name] = scenario
        return scenarios_dict

    def prePopulateDB(self):
        scenarios_to_add = ['Scenario_1', 'Scenario_3']
        currentScenarios = self.getScenarios()
        scenarios_list = [scenario['scenario_name'] for scenario in currentScenarios]
        scenarios_set = set(scenarios_list)
        for scenario_name in scenarios_to_add:
            if scenario_name not in scenarios_set:
                json_name = ''.join([scenario_name, ".json"])
                with open(self.file_manager.getJSONPath(scenario_name) / json_name) as outfile:
                    scenario_dict = json.load(outfile)
                scenario = Scenario(scenario_name).objectFromDictionary(scenario_dict)
                self.insertScenario(scenario.dictionary().copy())
        return

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
