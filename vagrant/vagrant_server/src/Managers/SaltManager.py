import subprocess
import os
import string
from Entities.MinionConfigFile import MinionConfigFile

class SaltManager():
    def __init__(self):
        self.m_conf_file = MinionConfigFile()
        return

    def generateMinionID(self,scenario_name, machine_name):
        minion_id = '_'.join([self._removeWhitespaces(scenario_name), self._removeWhitespaces(machine_name)])
        return minion_id

    def generateKeys(self, keys_path, minion_id):
        #Change directory to keys path
        os.chdir(keys_path)
        #Give permission to the salt user
        #print("Giving permission to the salt user")
        #command = ['sudo', 'chmod', 'a+rwx', '.']
        #self._runCommandFromShell(command)
        #Generate keys
        print("Generating keys for minion id: ", minion_id)
        command = ['sudo', 'salt-key', ''.join(['--gen-keys=', minion_id])]
        self._runCommandFromShell(command)
        #Add public key to the accepted minion folder
        #print("Copying the minion public key to the salt master public keys folder")
        #command = ['sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/var/lib/salt/pki/master/minions/', minion_id])]
        #self._runCommandFromShell(command)
        #command = ['sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/etc/salt/pki/master/minions/', minion_id])]
        #self._runCommandFromShell(command)
        return

    def acceptKeys(self, minion_id):
        print("Accepting key for minion id: ", minion_id)
        command = ['sudo', 'salt-key', '-a', minion_id, '-y']
        self._runCommandFromShell(command)
        return

    def generateMinionConfigFile(self, conf_path, minion_id):
        print("Generating Minion config file")
        return self.m_conf_file.generateMinionConfigFile(conf_path, minion_id)

    def _runCommandFromShell(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        return

    def _removeWhitespaces(self, s):
        return s.translate({ord(c): None for c in string.whitespace})