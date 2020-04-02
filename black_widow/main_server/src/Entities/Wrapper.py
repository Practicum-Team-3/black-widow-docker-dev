from Entities.Entity import Entity

class Wrapper(Entity):
    def __init__(self, response = "", code = "", status = "", task_id = "", body = ""):

        self.response = response
        self.code = code
        self.status = status
        self.task_id = task_id
        self.body = body

    def setCode(self, code):
        self.code =code
    
    def setStatus(self, status):
        self.status =status

    def setTask_id(self, task_id):
        self.task_id =task_id

    def setBody(self, body):
        self.body =body

    def setResponse(self, response):
        self.response =response
    

    def dictionary(self):
        """
        Generates a dictionary for the Wrapper object
        :return: A dictionary with Wrapper data
        """
        dicti = dict()
        dicti["response"] = self.response
        dicti["code"] = self.code
        dicti["status"] = self.status
        dicti["task_id"] = self.task_id
        dicti["body"] = self.body
        return dicti

    def objectFromDictionary(self, dict):
        self.response = dict["response"]
        self.code = dict["code"]
        self.status = dict["status"]
        self.task_id = dict["task_id"]
        self.body = dict["body"]
        return self