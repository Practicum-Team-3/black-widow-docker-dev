import subprocess
import os
from Entities.MinionConfigFile import MinionConfigFile

class SaltManager():
    def __init__(self):
        self.m_conf_file = MinionConfigFile()
        return

    def generateKeys(self, keys_path, minion_id):
        #Change directory to keys path
        os.chdir(keys_path)
        #Give permission to the salt user
        print("Giving permission to the salt user")
        command = ['sudo', 'chmod', 'a+rwx', '.']
        self._runCommandFromShell(command)
        #Generate keys
        print("Generating keys")
        command = ['sudo', 'salt-key', ''.join(['--gen-keys=', minion_id])]
        self._runCommandFromShell(command)
        #Add public key to the accepted minion folder
        print("Copying the minion public key to the salt master public keys folder")
        command = ['sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/var/lib/salt/pki/master/minions/', minion_id]) ]
        self._runCommandFromShell(command)
        command = ['sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/etc/salt/pki/master/minions/', minion_id]) ]
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
