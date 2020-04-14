import os
import subprocess
import re

if __name__ == "__main__":
    file_name = "cumulus-linux-4.1.0-vx-amd64-1584996322.6aca396zdd3fc1f8"
    ova_file = "".join([file_name, ".ova"])
    box_file = "".join([file_name, ".box"])

    #IMPORTING OVA FILE INTO VIRTUAL BOX
    #vboxmanage import cumulus-linux-4.1.0-vx-amd64-vbox.ova
    print('IMPORTING OVA FILE INTO VIRTUAL BOX')
    process = subprocess.Popen(['vboxmanage', 'import', ova_file], stdout=subprocess.PIPE,
                               universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    #GETTING VIRTUAL MACHINE ID
    #VBoxManage list vms
    print('GETTING VIRTUAL MACHINE ID')
    process = subprocess.Popen(['vboxmanage', 'list', 'vms'], stdout=subprocess.PIPE,
                               universal_newlines=True)
    box_id = ""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
        if file_name in output:
            box_id = output
    pattern = '(^.*{)(.+)(}.*)'
    match = re.search(pattern, box_id)
    box_id = match.group(2)
    print('Box id = ', box_id)

    #PACKAGING VIRTUAL MACHINE INTO A BOX
    #vagrant package --base cumulus-linux-4.1.0-vx-amd64-vbox.ova --output cumulus.box
    print('PACKAGING VIRTUAL MACHINE INTO A BOX')
    process = subprocess.Popen(['vagrant' , 'package', '--base', box_id, '--output', box_file], stdout=subprocess.PIPE,
                               universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    #ADDING BOX BY NAME
    #vagrant add box cumulus.box --name cumulus
    print('PACKAGING VIRTUAL MACHINE INTO A BOX')
    process = subprocess.Popen(['vagrant', 'box', 'add', box_file, '--name', file_name], stdout=subprocess.PIPE,
                               universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())