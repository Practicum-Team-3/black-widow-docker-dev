#!/bin/bash

# This script helps with the setup of the configuration that will be part of the black widow system.

pwd ./
WORKING_DIR=`pwd`
LOCAL_APP_PATH=$WORKING_DIR'/black_widow/main_server/src'
DESTINATION_APP='/opt/black_widow'
BW_DOCKERFILE_PATH='./black_widow'

rm -f .env
touch .env

rm -f $LOCAL_APP_PATH/.env
touch $LOCAL_APP_PATH/.env

rm -f $BW_DOCKERFILE_PATH/black_widow.env
touch $BW_DOCKERFILE_PATH/black_widow.env




reg='^[+]?[0-9]{0,5}$'

read -p 'Enter the port number that will be used by the Black Widow container, else press enter [Default=8080]: '  BW_CON_PORT
until [[  $BW_CON_PORT =~ $reg || $BW_CON_PORT == "" ]] ; do 
    echo 'Oops! Use input was not 5 digits as it should be'
    echo 
    read -p 'Enter the Black Widow container port once again' $BW_CON_PORT
done
if [[ $BW_CON_PORT = "" ]]; then 
    echo BW_CON_PORT=8080 | tee -a .env 
else 
    echo BW_CON_PORT=$BW_CON_PORT  | tee -a .env 
fi 

read -p 'Enter the port number that will be used by the Black Widow APP, else press enter [Default=5000]: '  BW_APP_PORT
until [[  $BW_APP_PORT =~ $reg || $BW_APP_PORT == "" ]] ; do 
    echo 'Oops! Use input was not 5 digits as it should be'
    echo 
    read -p 'Enter the Black Widow container port once again' $BW_APP_PORT
done
if [[ $BW_APP_PORT = "" ]]; then 
    echo BW_APP_PORT=5000  | tee -a .env $LOCAL_APP_PATH/.env
else 
    echo BW_APP_PORT=$BW_APP_PORT  | tee -a .env $LOCAL_APP_PATH/.env
fi 


DOCKER_HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
echo DOCKER_HOST=$DOCKER_HOST >> $LOCAL_APP_PATH/.env

echo LOCAL_APP_PATH=$LOCAL_APP_PATH >> .env
echo DESTINATION_APP=$DESTINATION_APP | tee -a .env 



