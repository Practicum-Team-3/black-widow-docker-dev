# Docker Development Environment
## Steps to follow:
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

