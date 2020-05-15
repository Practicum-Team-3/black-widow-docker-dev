from Entities.Entity import Entity


class Provision(Entity):
    def __init__(self, name="", provision_type="shell"):
        self.name = name
        self.provision_type = provision_type
        self.commands = list()

    def setShellCommand(self, command):
        """
        Sets a new command to be executed as part of the provisioning
        :param command: Bash command intended for provisioning a virtual machine
        """
        self.commands.append(command)

    def dictionary(self):
        """
        Generates a dictionary for the Provision object
        :return: A dictionary with Provision's data
        """
        dicti = dict()
        dicti["name"] = self.name
        dicti["provision_type"] = self.provision_type
        dicti["commands"] = self.commands
        return dicti

    def objectFromDictionary(self, dict):
        """
        Creates a Provision object from a dictionary.
        :param dict: A dictionary containing the Provision's data
        :return: A Provision object
        """
        self.name = dict["name"]
        self.provision_type = dict["provision_type"]
        self.commands = dict["commands"]
        return self