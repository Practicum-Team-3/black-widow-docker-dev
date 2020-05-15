# Docker Development Environment

## Steps to follow:

This environment has been tested on Ubuntu 18.04

1. Run the following script to install the dependencies of the project: <br/>
`sudo ./install-dependencies.sh`

2. Run this script to set up the environment: <br/>
`./setup.sh`

3. Run the following script to run the project: <br/>
`./run.sh` <br/>



****** THE INSTRUCTIONS BELOW ARE DEPRECATED BUT ARE STILL RELEVANT *******



1. Run the following script: <br/>
`./auto-setup.sh` <br/>
**Note:** 
*This script will set all the necesary environment variables for the docker container to set up. For a painless configuration, leave all the values by default* <br/>

2. Run the following script: <br/>
`./pip-install.sh`<br/>
**Note:** 
*This script pip installs all the necesary packages for the server to run on the host.* <br/>

3. Run the following script: <br/>
`sudo ./install-dependencies.sh`<br/>
**Note:** 
*This script will install tcl interpreter into your machine which is required for celery to work in our system* <br/>

3. Run the following script: <br/>
`./build.sh` <br/>
**Note:** 
*This script will create the containers by using the previously setup variables.* <br/>

4. Run the following script: <br/>
`./run.sh` <br/>
**Note:** 
*This script runs three parts of our system:  This is the equivalent of running the commands:* <br/>
`docker-compose up` <br/>
`python3 ./vagrant/src/VagrantServer.py` <br/>
`celery worker -A CeleryWorker.celery --loglevel=info `<br/>

