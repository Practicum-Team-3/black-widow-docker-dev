import subprocess

class ConsoleManager():
    def runCommandFromShell(self, command):
        print("\033[1;31;40mExecuting the following command: ")
        print(''.join(["\033[1;32;40m", ' '.join(command)]))
        process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(''.join(["\033[1;32;40m", output.strip()]))
        return

    def printRed(self, command):
        print(''.join(["\033[1;31;40m", command]))
        return

    def printGreen(self, command):
        print(''.join(["\033[1;32;40m", command]))
        return

    def printBlue(self, command):
        print(''.join(["\033[1;34;40m", command]))
        return