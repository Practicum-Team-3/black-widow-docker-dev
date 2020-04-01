from flask import Flask, jsonify, render_template, request
from werkzeug import secure_filename
import os

""" Modified from https://github.com/twtrubiks/flask-dropzone-wavesurfer"""

uploadfiles = Flask(__name__)
UPLOAD_PATH = 'Files/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_PATH)
UPLOAD_F = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_PATH)
files_dict = dict()

#TODO: Set appropiate paths to files.

#TODO: POST parameter for the type of file 
#TODO: MAke a different folder to  add the stuff

@uploadfiles.route('/')
def index():
    all_VMs = []
    all_exploits = []
    all_vagrantfiles = []
    all_image_files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        ## Check for VMs
        if (isVMFormat(filename)):
            all_VMs.append(filename)
        ## Exploits
        if (isExploitFormat(filename)):
            all_exploits.append(filename)
   
    return render_template('index.html', **locals());


def isVMFormat(link):
    if (link.find('.ova') > -1):
        return 'Virtual Machines';
    return;

def isExploitFormat(link):
    if (link.find('.txt') > -1 or link.find('.go') > -1 or link.find('.py') > -1):
        return 'Exploits';
    return;
    
def isVulnerabilityFormat(link):
    if (link.find('.zip') > -1 or link.find('.tar.gz') > -1 or link.find('.rar') > -1 or link.find('.7z') > -1):
        return 'Vulnerable Software';
    return;

def filePath(link):
    return UPLOAD_FOLDER + isVMFormat(link) + isExploitFormat(link) + isVulnerabilityFormat(link);

# curl -X POST -F "file=@/path/to/file.ext" http://localhost:5000/uploadFile
@uploadfiles.route('/uploadFile', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        file = request.files['file']
        
        if os.path.isfile(UPLOAD_PATH + file.filename):
            return 'File already exists'
        upload_path = '{}/{}'.format(UPLOAD_FOLDER, secure_filename(file.filename))

        file.save(upload_path)
        return 'File Successfully Uploaded'
    
@uploadfiles.route('/deleteFile/<file_name>')
def deleteFile(file_name):
    file = UPLOAD_PATH + file_name
    if os.path.isfile(file):
        os.remove(file)
        return 'File Successfully Deleted'
    else:    ## Show an error ##
        return 'File not found, could not delete'
    
#    if file_name in files_dict:
#        deleted_scenario = files_dict.pop(file_name)
#        scenario_path = self.file_manager.getScenariosPath() / file_name
#        try:
#            shutil.rmtree(scenario_path)
#        except OSError as e:
#            print("Error: %s : %s" % (scenario_path, e.strerror))
#        return {"Response": True, "Note": "Operation successful",
#                "Body": deleted_scenario.dictionary()}
#    else:
#        return {"Response": False, "Note": "Scenario doesn't exist" , "Body": dict()}

def getFileList():
    all_VMs = []
    all_exploits = []
    all_vulnerable_software = []
    for filename in os.listdir(UPLOAD_FOLDER):
        ## Check for VMs
        if (isVMFormat(filename)):
            all_VMs.append(filename)
        ## Exploits
        if (isExploitFormat(filename)):
            all_exploits.append(filename)
        ## Vulnerable Software
        if (isVulnerabilityFormat(filename)):
            all_vulnerable_software.append(filename)
    return all_VMs, all_exploits, all_vulnerable_software

@uploadfiles.route('/fileList/')
def fileList():
    all_VMs, all_exploits, all_vulnerable_software = getFileList()
    files_dict = {"virtual machines": all_VMs,
                  "exploits": all_exploits,
                  "vulnerable software": all_vulnerable_software}
    return jsonify(files_dict)
        
        
if __name__ == '__main__':
    uploadfiles.run(debug=False)
