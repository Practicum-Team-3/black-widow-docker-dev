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
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
'''
mongodb_ip = settings.mongodb_ip
mongodb_port = settings.mongodb_port
db_name = settings.db_name
mongodb_username = settings.mongodb_username
mongdb_password = settings.mongdb_password
mongodb_url = "mongodb://" + mongodb_ip + ":" + mongodb_port
'''
MONGOD_IP = settings.mongodb_ip
MONGOD_PORT = settings.mongodb_port

DB_NAME = settings.db_name
MONGODB_USERNAME = settings.mongodb_username
MONGODB_PASSWORD = settings.mongdb_password
MONGODB_HOSTNAME = settings.mongodb_hostname
#MONGODB_URL = "mongodb://" + MONGOD_IP + ":" + MONGOD_PORT
print(MONGOD_IP, MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOSTNAME, MONGOD_PORT, DB_NAME)
MONGODB_URL = "mongodb://" + MONGODB_USERNAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOSTNAME + ":" + MONGOD_PORT + "/" + DB_NAME
print(MONGODB_URL)


class DatabaseManager():

    def __init__(self):
        self.url = MONGODB_URL
        self.db_name = DB_NAME
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
