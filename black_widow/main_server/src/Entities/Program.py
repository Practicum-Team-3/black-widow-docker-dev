from Entities.Entity import Entity

class Program(Entity):
    def __init__(self, name="", location=""):
        self.name = name
        self.location = location

    def dictionary(self):
        """
        Generates a dictionary for the Program object
        :return: A dictionary with Program's data
        """
        dicti = dict()
        dicti["name"] = self.name
        dicti["location"] = self.location
        return dicti

    def objectFromDictionary(self, dict):
        """
        Creates an Program object from a dictionary.
        :param dict: A dictionary containing the Program's data
        :return: A Program object
        """
        self.name = dict["name"]
        self.location = dict["location"]
        return self