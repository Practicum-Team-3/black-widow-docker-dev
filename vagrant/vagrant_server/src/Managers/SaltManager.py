import os
import subprocess
import re
from CeleryApp import celery
from Managers.FileManager import FileManager
from Managers.DatabaseManager import DatabaseManager
from Entities.VagrantFile import VagrantFile
from Entities.Response import Response

file_manager = FileManager()
db_manager = DatabaseManager()
vagrant_file = VagrantFile()

class SaltManager():
    def generateKeys(self, keys_path, minion_id):
        #Access to salt user
        #command = ['sudo', 'cd', keys_path]
        #self._runCommandFromShell(command)
        #Access to salt user
        command = ['sudo', 'chmod', 'a+rwx', '.']
        self._runCommandFromShell(command)
        #Generate keys
        command = ['sudo', 'salt-key', ''.join(['--gen-keys=', minion_id])]
        self._runCommandFromShell(command)
        #Add public key to the accepted minion folder
        command = [ 'sudo', 'cp', ''.join([minion_id, '.pub']), ''.join(['/etc/salt/pki/master/minions/', minion_id]) ]
        self._runCommandFromShell(command)
        #Move keys to keys folder
        command = [ 'sudo', 'mv', ''.join([minion_id, '.pub']), ''.join([minion_id, '.pem']), './saltstack/keys' ]
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