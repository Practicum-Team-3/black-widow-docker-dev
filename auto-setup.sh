#!/bin/bash

# This script helps with the setup of the configuration that will be part of the black widow system.

pwd ./
WORKING_DIR=`pwd`
LOCAL_APP_PATH=$WORKING_DIR'/black_widow/main_server/src'
DESTINATION_APP='/opt/black_widow'
BW_DOCKERFILE_PATH='./black_widow'
VAGRANT_PATH=$WORKING_DIR'/vagrant/vagrant_server/src'

rm -f .env
touch .env

rm -f $LOCAL_APP_PATH/.env
touch $LOCAL_APP_PATH/.env

rm -f $VAGRANT_PATH/.env
touch $VAGRANT_PATH/.env

rm -f $BW_DOCKERFILE_PATH/black_widow.env
touch $BW_DOCKERFILE_PATH/black_widow.env

SUBNET_WIDOW=172.18.128.0 
echo SUBNET_WIDOW=$SUBNET_WIDOW  | tee -a .env 

WIDOW_IP=172.18.128.2
echo WIDOW_IP=$WIDOW_IP | tee -a .env 

BW_CON_PORT=8080
echo BW_CON_PORT=$BW_CON_PORT  | tee -a .env 

REDIS_HOST=172.18.128.7 
echo REDIS_HOST=$REDIS_HOST | tee -a .env $VAGRANT_PATH/.env


REDIS_PORT=6379
echo REDIS_PORT=$REDIS_PORT  | tee -a .env $VAGRANT_PATH/.env

BW_APP_PORT=5000
echo BW_APP_PORT=$BW_APP_PORT  | tee -a .env $LOCAL_APP_PATH/.env

MONGODB_IP=172.18.128.3 |
echo MONGODB_IP=$MONGODB_IP  | tee -a .env $LOCAL_APP_PATH/.env $VAGRANT_PATH/.env

MONGODB_PORT=27017
echo MONGODB_PORT=$MONGODB_PORT | tee -a .env $LOCAL_APP_PATH/.env $VAGRANT_PATH/.env

MONGODB_DATABASE=softpract  
echo MONGODB_DATABASE=$MONGODB_DATABASE | tee -a .env 

MONGODB_USERNAME=widowuser
echo MONGODB_USERNAME=$MONGODB_USERNAME | tee -a .env 

MONGODB_PASSWORD=mongodb_password
echo MONGODB_PASSWORD=$MONGODB_PASSWORD | tee -a .env 



MONGODB_ROOT_USER=rootuser
echo MONGODB_ROOT_USER=$MONGODB_ROOT_USER | tee -a .env $LOCAL_APP_PATH/.env $VAGRANT_PATH/.env

MONGODB_ROOT_PASSWORD=your_mongodb_password
echo MONGODB_ROOT_PASSWORD=$MONGODB_ROOT_PASSWORD | tee -a .env $LOCAL_APP_PATH/.env $VAGRANT_PATH/.env

MONGODB_HOSTNAME=mongodb
echo MONGODB_HOSTNAME=$MONGODB_HOSTNAME | tee -a .env $LOCAL_APP_PATH/.env

ENVIRONMENT_DEBUG=false
echo ENVIRONMENT_DEBUG=$ENVIRONMENT_DEBUG | tee -a .env $LOCAL_APP_PATH/.env


DOCKER_HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
echo DOCKER_HOST=$DOCKER_HOST >> $LOCAL_APP_PATH/.env 

echo LOCAL_APP_PATH=$LOCAL_APP_PATH >> .env
echo DESTINATION_APP=$DESTINATION_APP | tee -a .env 




