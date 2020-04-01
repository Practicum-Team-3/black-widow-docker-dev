from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

""" Modified from https://github.com/twtrubiks/flask-dropzone-wavesurfer"""

uploadfiles = Flask(__name__)
UPLOAD_PATH = 'Files/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_PATH)
UPLOAD_F = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_PATH)

#TODO: Handle VagrantFiles, VMs, exploits (zip, 7z, etc.) or just everything?
#TODO: get existing files??
#TODO: Set appropiate paths to files. 
#TODO: See what the scope of what I need to do is.
#TODO: Vulnerable programs

#TODO: POST parameter for the type of file 
#TODO: Return file list in 
#TODO: MAke a different folder to  add the stuff

#TODO: DELETRION OF FILES
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

#curl -X POST -F "file=@ts.png" http://localhost:5000/upload
@uploadfiles.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        upload_path = '{}/{}'.format(UPLOAD_FOLDER, secure_filename(file.filename))

        file.save(upload_path)
        return 'ok'
    

if __name__ == '__main__':
    uploadfiles.run(debug=False)
