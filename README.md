# Docker Development Environment
## Steps to follow:
1. Run the following script: <br/>
`./setup.sh` <br/>
**Note:** 
*This script will set all the necesary environment variables for the docker container to set up.* <br/>

2. Run the following script: <br/>
`./pip-install.sh`<br/>
**Note:** 
*This script pip installs all the necesary packages for the server to run on the host.* <br/>

3. Run the following script: <br/>
`./build.sh` <br/>
**Note:** 
*This script will create the containers by using the previously setup variables.* <br/>

4. Run the following script: <br/>
`./run.sh` <br/>
**Note:** 
*This script runs both servers. This is the equivalent of running the commands:* <br/>
`docker-compose up` <br/>
`python3 ./vagrant/src/VagrantServer.py` <br/>

5. Once the script has finished run: <br/>
`sudo shutdown now -r`