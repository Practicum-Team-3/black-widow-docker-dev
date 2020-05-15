from Entities.Entity import Entity

class Response(Entity):
    def __init__(self, response="", reason="", status="", task_id="", body=""):
        self.response = response
        self.reason = reason
        self.status = status
        self.task_id = task_id
        self.body = body

    def setReason(self, reason):
        """
        Sets success/fail reason of a request.
        :param reason: String containing the request's reason
        """
        self.reason = reason

    def setStatus(self, status):
        """
        Set the status of a request.
        :param status: String containing the request's status
        """
        self.status = status

    def setTaskID(self, task_id):
        """
        Sets the task ID of a request.
        :param task_id: String containing the request's task id
        """
        self.task_id = task_id

    def setBody(self, body):
        """
        Sets the body of a request.
        :param: String containing the request's body
        """
        self.body = body

    def setResponse(self, response):
        """
        Sets the response of a request.
        :param response: String containing the request's response
        """
        self.response = response

    def dictionary(self):
        """
        Generates a dictionary for the Response object
        :return: A dictionary with Response data
        """
        dicti = dict()
        dicti["response"] = self.response
        dicti["reason"] = self.reason
        dicti["status"] = self.status
        dicti["task_id"] = self.task_id
        dicti["body"] = self.body
        return dicti

    def objectFromDictionary(self, dict):
        """
        Creates a Response object from a dictionary.
        :param dict: A dictionary containing the Response data
        :return: A Response object
        """
        self.response = dict["response"]
        self.reason = dict["reason"]
        self.status = dict["status"]
        self.task_id = dict["task_id"]
        self.body = dict["body"]
        return self