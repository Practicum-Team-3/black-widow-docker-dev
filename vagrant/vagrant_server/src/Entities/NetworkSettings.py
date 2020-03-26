class NetworkSettings(object):
    def __init__(self , network_name , network_type , ip_address , auto_config=True):
        self.network_name = network_name
        self.network_type = network_type
        self.ip_address = ip_address
        self.auto_config = auto_config
        
    def dictionary(self):
        """
        Generates a dictionary for the NetworkSettings object
        :return: A dictionary with NetworkSettings data
        """
        n_dict = dict()
        n_dict["network_name"] = self.network_name
        n_dict["network_type"] = self.network_type
        n_dict["ip_address"] = self.ip_address
        n_dict["auto_config"] = self.auto_config
        return n_dict