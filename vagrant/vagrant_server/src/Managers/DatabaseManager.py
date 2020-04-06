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
from Managers.ConfigManager import ConfigManager

class DatabaseManager():

    def __init__(self):
        self.url = ConfigManager().mongoURL()
        self.db_name = "soft_prac"
        self.scenarios_col_name = 'scenarios'
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[self.db_name]
        self.scenarios_col = self.db[self.scenarios_col_name]

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
