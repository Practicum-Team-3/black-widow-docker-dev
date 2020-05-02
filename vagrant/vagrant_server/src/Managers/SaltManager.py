import subprocess
import os

class SaltManager():

    def generateKeys(self, keys_path, minion_id):
        #Change directory to keys path
        os.chdir(keys_path)
        #Access to salt user
        command = ['sudo', 'chmod', 'a+rwx', '.']
        self._runCommandFromShell(command)
        #Generate keys
        command = ['sudo', 'salt-key', ''.join(['--gen-keys=', minion_id])]
        self._runCommandFromShell(command)
        #Add public key to the accepted minion folder
        command = [ 'sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/var/lib/salt/pki/master/minions/', minion_id]) ]
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