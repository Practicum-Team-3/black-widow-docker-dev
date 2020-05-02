#!/bin/bash
WORKING_DIR=`pwd`
VAGRANT_DIR=$WORKING_DIR/vagrant/vagrant_server/src/

docker-compose down
docker network prune -y
gnome-terminal -- bash -c "docker-compose up mongodb redis black_widow"
gnome-terminal -- bash -c "cd $VAGRANT_DIR; celery worker -A CeleryWorker.celery --loglevel=info"
gnome-terminal -- bash -c "cd $VAGRANT_DIR; python3 VagrantServer.py"

