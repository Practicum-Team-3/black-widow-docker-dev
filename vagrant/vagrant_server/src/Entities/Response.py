from Entities.Entity import Entity

class Response(Entity):
    def __init__(self, response="", reason="", status="", task_id="", body=""):
        self.response = response
        self.reason = reason
        self.status = status
        self.task_id = task_id
        self.body = body

    def setReason(self, reason):
        self.reason = reason

    def setStatus(self, status):
        self.status = status

    def setTaskID(self, task_id):
        self.task_id = task_id

    def setBody(self, body):
        self.body = body

    def setResponse(self, response):
        self.response = response

    def dictionary(self):
        """
        Generates a dictionary for the Wrapper object
        :return: A dictionary with Wrapper data
        """
        dicti = dict()
        dicti["response"] = self.response
        dicti["reason"] = self.reason
        dicti["status"] = self.status
        dicti["task_id"] = self.task_id
        dicti["body"] = self.body
        return dicti

    def objectFromDictionary(self, dict):
        self.response = dict["response"]
        self.reason = dict["reason"]
        self.status = dict["status"]
        self.task_id = dict["task_id"]
        self.body = dict["body"]
        return self