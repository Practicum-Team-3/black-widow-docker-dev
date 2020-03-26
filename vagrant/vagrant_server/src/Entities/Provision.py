class Provision(object):
    def __init__(self, name, provision_type = "shell"):
        self.name = name
        self.provision_type = provision_type
        self.commands = list()
    
    def setShellCommand(self, command ):
        """
        Sets a new command to be executed as part of the provisioning
        :param command: Bash command intended for provisioning a virtual machine
        """
        self.commands.append(command)
        
    def dictionary(self):
        """
        Generates a dictionary for the Provision object
        :return: A dictionary with Provision data
        """
        prov_dict = dict()
        prov_dict["name"] = self.name
        prov_dict["provision_type"] = self.provision_type
        prov_dict["commands"] = self.commands
        return prov_dict