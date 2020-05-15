import pymongo
from Managers.ConfigManager import ConfigManager

class DatabaseManager():

    def __init__(self):
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

    #CRUD: CREATE, READ, UPDATE and DELETE

    #Scenarios
    def insertScenario(self, scenario_json):
        """
        Inserts a scenario into the database.
        :param scenario_json: Scenario's JSON file to be inserted
        :return: Inserted document's id
        """
        doc = self.scenarios_col.insert_one(scenario_json)
        return doc.inserted_id

    def getScenarioNames(self):
        """
        Gets the scenario's names.
        :return: A list containing the scenarios names
        """
        return [doc['scenario_name'] for doc in self.scenarios_col.find()]

    def getScenarios(self):
        """
        Gets the scenarios from the databases.
        :return: A list containing scenarios in the database
        """
        return [doc for doc in self.scenarios_col.find()]

    def getScenario(self, scenario_name):
        """
        Gets a specific scenario from the database.
        :param scenario_name: Scenario's name string
        :return: A list containing the scenario retrieved from the database
        """
        query = {'scenario_name': scenario_name}
        return [doc for doc in self.scenarios_col.find(query)]

    def editScenario(self, scenario_json):
        """
        Edits a scenario in the database.
        :param scenario_json: JSON file containing scenario's data
        :return: Modified document's id
        """
        query = {'scenario_name': scenario_json['scenario_name']}
        new_doc = {"$set": scenario_json }
        doc = self.scenarios_col.update_one(query, new_doc)
        return doc.modified_count

    def deleteScenario(self, scenario_name):
        """
        Deletes a scenario from the database.
        :param scenario_name: Scenario's name string
        :return: Deleted document's id
        """
        query = {'scenario_name': scenario_name}
        doc = self.scenarios_col.delete_one(query)
        return doc.deleted_count

    #Exploits
    def insertExploit(self, exploit_json):
        """
        Inserts a scenario in the database.
        :param exploit_json: JSON file containing the exploit's data
        :return: Inserted document's id
        """
        doc = self.exploits_col.insert_one(exploit_json)
        return doc.inserted_id

    def getExploitNames(self):
        """
        Gets the exploits names from the database.
        :return: A list containing the exploits' names
        """
        return [doc['name'] for doc in self.exploits_col.find()]

    def getExploits(self):
        """
        Gets the exploits stored in the database.
        :return: A list containing the stored exploits' data
        """
        return [doc for doc in self.exploits_col.find()]

    def getExploit(self, exploit_name):
        """
        Gets an exploit from the database.
        :param exploit_name: Exploit's name string
        :return: A list containing the exploit data
        """
        query = {'name': exploit_name}
        return [doc for doc in self.exploits_col.find(query)]

    def editExploit(self, exploit_json):
        """
        Edits an exploit in the database.
        :param exploit_json: JSON file containing the exploit's data
        :return: Modified document's id
        """
        query = {'name': exploit_json['name']}
        new_doc = {"$set": exploit_json }
        doc = self.exploits_col.update_one(query, new_doc)
        return doc.modified_count

    def deleteExploit(self, exploit_name):
        """
        Deletes a exploit from the database.
        :param exploit_name: Exploit's name string
        :return: Deleted document's id
        """
        query = {'name': exploit_name}
        doc = self.exploits_col.delete_one(query)
        return doc.deleted_count

    #Vulnerabilities
    def insertVulnerability(self, vulnerability_json):
        """
        Inserts a vulnerability in the database.
        :param vulnerability_json: JSON file containing the vulnerability's data
        :return: Inserted document's id
        """
        doc = self.vulnerabilities_col.insert_one(vulnerability_json)
        return doc.inserted_id

    def getVulnerabilityNames(self):
        """
        Gets the vulnerabilities names from the database.
        :return: A list containing the vulnerability's names
        """
        return [doc['name'] for doc in self.vulnerabilities_col.find()]

    def getVulnerabilities(self):
        """
        Gets the vulnerabilities stored in the database.
        :return: A list containing the stored vulnerabilities' data
        """
        return [doc for doc in self.vulnerabilities_col.find()]

    def getVulnerability(self, vulnerability_name):
        """
        Gets a vulnerability from the database.
        :param vulnerability_name: Vulnerability's name string
        :return: A list containing the vulnerability's data
        """
        query = {'name': vulnerability_name}
        return [doc for doc in self.vulnerabilities_col.find(query)]

    def editVulnerability(self, vulnerability_json):
        """
        Edits a vulnerability in the database.
        :param vulnerability_json: JSON file containing the vulnerability's data
        :return: Modified document's id
        """
        query = {'name': vulnerability_json['name']}
        new_doc = {"$set": vulnerability_json }
        doc = self.vulnerabilities_col.update_one(query, new_doc)
        return doc.modified_count

    def deleteVulnerability(self, vulnerability_name):
        """
        Deletes a vulnerability from the database.
        :param vulnerability_name: Vulnerability's name string
        :return: Deleted document's id
        """
        query = {'name': vulnerability_name}
        doc = self.vulnerabilities_col.delete_one(query)
        return doc.deleted_count
