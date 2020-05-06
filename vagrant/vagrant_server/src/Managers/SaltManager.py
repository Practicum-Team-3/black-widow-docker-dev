import subprocess
import os
import string
from Entities.MinionConfigFile import MinionConfigFile

class SaltManager():
    def __init__(self):
        self.m_conf_file = MinionConfigFile()
        return

    def generateMinionID(self, machine_name):
        minion_id = self._removeWhitespaces(machine_name)
        return minion_id

    def generateMinionConfigFile(self, conf_path, minion_id):
        print("Generating Minion config file")
        return self.m_conf_file.generateMinionConfigFile(conf_path, minion_id)

    def generateKeys(self, keys_path, minion_id):
        #Change directory to keys path
        os.chdir(keys_path)
        #Give permission to the salt user
        print("Giving permission to the salt user")
        command = ['sudo', 'chmod', 'a+rwx', '.']
        self._runCommandFromShell(command)
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

    def runSaltHighstate(self, minion_id):
        print("Running salt highstate: ", minion_id)
        command = ['sudo', 'salt', minion_id, 'state.apply']
        self._runCommandFromShell(command)
        return

    def copyingBeatsConfigFiles(self, minion_id):
        print("Copying beats config files: ", minion_id)
        #Filebeat state
        command = ['sudo', 'salt', minion_id, 'cp.get_file', 'salt://conf/filebeat.yml', '/etc/filebeat/']
        self._runCommandFromShell(command)
        #Restart filebeat service
        command = ['sudo', 'salt', minion_id, 'cmd.run', 'sudo service filebeat restart']
        self._runCommandFromShell(command)
        #Metricbeat state
        command = ['sudo', 'salt', minion_id, 'cp.get_file', 'salt://conf/metricbeat.yml', '/etc/metricbeat/']
        self._runCommandFromShell(command)
        #Restart metricbeat service
        command = ['sudo', 'salt', minion_id, 'cmd.run', 'sudo service metricbeat restart']
        self._runCommandFromShell(command)
        return

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