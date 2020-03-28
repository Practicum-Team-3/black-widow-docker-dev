# Docker Development Environment

Run:
### This script will set all the necesary environment variables for the docker container to set up.
./setup.sh
### This script pip installs all the necesary packages for the server to run on the host
./pip-install.sh
### This script will create the containers by using the previously setup variables
./build.sh
### This script runs both servers. This is the equivalent of running the commands:
#### docker-compose up
#### python3 ./vagrant/src/VagrantServer.py
./run.sh

Once the script has finished run:

sudo shutdown now -r