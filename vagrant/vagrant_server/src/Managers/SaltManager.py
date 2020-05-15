import os
import string
from Entities.MinionConfigFile import MinionConfigFile
from Managers.ConsoleManager import ConsoleManager

class SaltManager():

    def __init__(self):
        self.m_conf_file = MinionConfigFile()
        self.console_manager = ConsoleManager()
        return

    def generateMinionID(self, machine_name):
        """
        Generates a minion id.
        :param machine_name: Machine's name string
        :return: A minion's id
        """
        minion_id = self._removeWhitespaces(machine_name)
        return minion_id

    def generateMinionConfigFile(self, conf_path, minion_id):
        """
        Generates a minion config file.
        :param conf_path: Path where the config file will be stored.
        :param minion_id: The minion's id
        :return: String with the config minion file data
        """
        self.console_manager.printRed("Generating minion config file")
        return self.m_conf_file.generateMinionConfigFile(conf_path, minion_id)

    def generateKeys(self, keys_path, minion_id):
        """
        Generates the keys for a specific minion.
        :param keys_path: Path where the keys will be stored
        :param minion_id: The minion's id
        :return: None
        """
        #Change directory to keys path
        os.chdir(keys_path)
        #Give permission to the salt user
        self.console_manager.printRed("Giving permission to the salt user")
        command = ['sudo', 'chmod', 'a+rwx', '.']
        self.console_manager.runCommandFromShell(command)
        #Generate keys
        self.console_manager.printRed(''.join(["Generating keys for minion id: ", minion_id]))
        command = ['sudo', 'salt-key', ''.join(['--gen-keys=', minion_id])]
        self.console_manager.runCommandFromShell(command)
        #Give permission to the salt user
        self.console_manager.printRed("Allowing vagrant to handle private keys")
        command = ['sudo', 'chmod', 'a+rwx', ''.join([minion_id, '.pub']), ''.join([minion_id, '.pem'])]
        self.console_manager.runCommandFromShell(command)
        #Add public key to the accepted minion folder
        self.console_manager.printRed("Copying the minion public key to the salt master public keys folder")
        command = ['sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/var/lib/salt/pki/master/minions/', minion_id])]
        self.console_manager.runCommandFromShell(command)
        command = ['sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/etc/salt/pki/master/minions/', minion_id])]
        self.console_manager.runCommandFromShell(command)
        return

    def acceptKeys(self, minion_id):
        """
        Accepts the public keys for a specific minion.
        :param minion_id: The minion's id
        :return: None
        """
        self.console_manager.printRed(''.join(["Accepting key for minion id: ", minion_id]))
        command = ['sudo', 'salt-key', '-a', minion_id, '-y']
        self.console_manager.runCommandFromShell(command)
        return

    def testPing(self, minion_id):
        """
        Pings a minion id to check connection.
        :param minion_id: The minion's id
        :return: None
        """
        self.console_manager.printRed(''.join(["Ping minion id: ", minion_id]))
        command = ['sudo', 'salt', minion_id, 'test.ping']
        self.console_manager.runCommandFromShell(command)
        return

    def runSaltHighstate(self, minion_id):
        """
        Runs the high state on a specific minion.
        :param minion_id: The minion's id
        :return: None
        """
        self.console_manager.printRed(''.join(["Running salt highstate: ", minion_id]))
        command = ['sudo', 'salt', minion_id, 'state.apply']
        self.console_manager.runCommandFromShell(command)
        return

    def copyingBeatsConfigFiles(self, minion_id):
        """
        Copies the beats config files into
        :param minion_id: The minion's id
        :return: None
        """
        self.console_manager.printRed(''.join(["Copying beats config files: ", minion_id]))
        #Filebeat state
        command = ['sudo', 'salt', minion_id, 'cp.get_file', 'salt://conf/filebeat.yml', '/etc/filebeat/']
        self.console_manager.runCommandFromShell(command)
        #Restart filebeat service
        command = ['sudo', 'salt', minion_id, 'cmd.run', '\"sudo service filebeat restart\"']
        self.console_manager.runCommandFromShell(command)
        #Print filebeat version
        command = ['sudo', 'salt', minion_id, 'cmd.run', '\"filebeat version\"']
        self.console_manager.runCommandFromShell(command)
        #Metricbeat state
        command = ['sudo', 'salt', minion_id, 'cp.get_file', 'salt://conf/metricbeat.yml', '/etc/metricbeat/']
        self.console_manager.runCommandFromShell(command)
        #Restart metricbeat service
        command = ['sudo', 'salt', minion_id, 'cmd.run', '\"sudo service metricbeat restart\"']
        self.console_manager.runCommandFromShell(command)
        #Print metricbeat version
        command = ['sudo', 'salt', minion_id, 'cmd.run', '\"metricbeat version\"']
        self.console_manager.runCommandFromShell(command)
        return

    def _removeWhitespaces(self, s):
        """
        Removes the whitespaces from a string.
        :param s: String to be processed
        :return: String processed
        """
        return s.translate({ord(c): None for c in string.whitespace})
