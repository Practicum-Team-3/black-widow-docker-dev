from Entities.Entity import Entity


class NetworkSettings(Entity):

    def __init__(self, network_name="", network_type="", ip_address="", auto_config=True):
        self.network_name = network_name
        self.network_type = network_type
        self.ip_address = ip_address
        self.auto_config = auto_config

    def dictionary(self):
        """
        Generates a dictionary for the NetworkSettings object
        :return: A dictionary with NetworkSettings' data
        """
        dicti = dict()
        dicti["network_name"] = self.network_name
        dicti["network_type"] = self.network_type
        dicti["ip_address"] = self.ip_address
        dicti["auto_config"] = self.auto_config
        return dicti

    def objectFromDictionary(self, dict):
        """
        Creates an NetworkSettings object from a dictionary.
        :param dict: A dictionary containing the NetworkSettings' data
        :return: A NetworkSettings object
        """
        self.network_name = dict["network_name"]
        self.network_type = dict["network_type"]
        self.ip_address = dict["ip_address"]
        self.auto_config = dict["auto_config"]
        return self