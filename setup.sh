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




numReg='^[+]?[0-9]{0,5}$'
alphaNumReg='^[a-zA-Z0-9][-a-zA-Z0-9]{0,15}[a-zA-Z0-9]$'
passwordReg='(?=(.*[A-Z]){4,})'

read -p 'Enter the port number that will be used by the Black Widow container, else press enter [Default=8080]: '  BW_CON_PORT
until [[  $BW_CON_PORT =~ $numReg || $BW_CON_PORT == "" ]] ; do 
    echo 'Oops! Use input was not 5 digits as it should be'
    echo 
    read -p 'Enter the Black Widow container port once again' BW_CON_PORT
done
if [[ $BW_CON_PORT = "" ]]; then 
    echo BW_CON_PORT=8080 | tee -a .env 
else 
    echo BW_CON_PORT=$BW_CON_PORT  | tee -a .env 
fi 

read -p 'Enter the port number that will be used by the Black Widow APP, else press enter [Default=5000]: '  BW_APP_PORT
until [[  $BW_APP_PORT =~ $numReg || $BW_APP_PORT == "" ]] ; do 
    echo 'Oops! Use input was not 5 digits as it should be'
    echo 
    read -p 'Enter the Black Widow container port once again' BW_APP_PORT
done
if [[ $BW_APP_PORT = "" ]]; then 
    echo BW_APP_PORT=5000  | tee -a .env $LOCAL_APP_PATH/.env
else 
    echo BW_APP_PORT=$BW_APP_PORT  | tee -a .env $LOCAL_APP_PATH/.env
fi 

read -p 'Enter the name of the database that will be set up for the app [Default=softpract] '  MONGODB_DATABASE
until [[  $MONGODB_DATABASE =~ $alphaNumReg || $MONGODB_DATABASE == "" ]] ; do 
    echo 'Oops! the name of the mongo database should be between 4 to 15 characters long. Only use alpha numeric characters'
    echo 
    read -p 'Enter the name of the database once again' MONGODB_DATABASE
done
if [[ $MONGODB_DATABASE = "" ]]; then 
    echo MONGODB_DATABASE=softpract  | tee -a .env #$LOCAL_APP_PATH/.env
else 
    echo MONGODB_DATABASE=$MONGODB_DATABASE | tee -a .env #$LOCAL_APP_PATH/.env
fi 

read -p 'Enter the username for mongo [Default=widowuser] '  MONGODB_USERNAME
until [[  $MONGODB_USERNAME =~ $alphaNumReg || $MONGODB_USERNAME == "" ]] ; do 
    echo 'Oops! the username of the mongo database should be between 4 to 15 characters long. Only use alpha numeric characters'
    echo 
    read -p 'Enter the name of the database once again' MONGODB_USERNAME
done
if [[ $MONGODB_USERNAME = "" ]]; then 
    echo MONGODB_USERNAME=widowuser  | tee -a .env #$LOCAL_APP_PATH/.env
else 
    echo MONGODB_USERNAME=$MONGODB_USERNAME | tee -a .env #$LOCAL_APP_PATH/.env
fi 

read -p 'Enter the password for the mongo database user [Default=mongodb_password] '  MONGODB_PASSWORD
until [[  $MONGODB_PASSWORD =~ $passwordReg || $MONGODB_PASSWORD == "" ]] ; do 
    echo 'Oops! the name of the database should be a minimum of 4 characters long long.'
    echo 
    read -p 'Enter the name of the database once again' MONGODB_PASSWORD
done
if [[ $MONGODB_PASSWORD = "" ]]; then 
    echo MONGODB_PASSWORD=mongodb_password  | tee -a .env #$LOCAL_APP_PATH/.env
else 
    echo MONGODB_PASSWORD=$MONGODB_PASSWORD | tee -a .env #$LOCAL_APP_PATH/.env
fi 


read -p 'Enter the ROOT username for the database [Default=rootuser] '  MONGODB_ROOT_USER
until [[  $MONGODB_ROOT_USER =~ $alphaNumReg || $MONGODB_ROOT_USER == "" ]] ; do 
    echo 'Oops! the name of the database should be between 4 to 15 characters long. Only use alpha numeric characters'
    echo 
    read -p 'Enter the name of the database once again' MONGODB_ROOT_USER
done
if [[ $MONGODB_ROOT_USER = "" ]]; then 
    echo MONGODB_ROOT_USER=rootuser  | tee -a .env #$LOCAL_APP_PATH/.env
else 
    echo MONGODB_ROOT_USER=$MONGODB_ROOT_USER | tee -a .env #$LOCAL_APP_PATH/.env
fi

read -p 'Enter the ROOT password for the database [Default=root_password] '  MONGODB_ROOT_PASSWORD
until [[  $MONGODB_ROOT_PASSWORD =~ $passwordReg || $MONGODB_ROOT_PASSWORD == "" ]] ; do 
    echo 'Oops! the name of the database should be a minimum of 4 characters long. Only use alpha numeric characters'
    echo 
    read -p 'Enter the name of the database once again' MONGODB_ROOT_PASSWORD
done
if [[ $MONGODB_ROOT_PASSWORD = "" ]]; then 
    echo MONGODB_ROOT_PASSWORD=your_mongodb_password  | tee -a .env #$LOCAL_APP_PATH/.env
else 
    echo MONGODB_ROOT_PASSWORD=$MONGODB_ROOT_PASSWORD | tee -a .env #$LOCAL_APP_PATH/.env
fi

read -p 'Enter the mongodb hostname [Default=mongodb] '  MONGODB_HOSTNAME
until [[  $MONGODB_HOSTNAME =~ $alphaNumReg || $MONGODB_HOSTNAME == "" ]] ; do 
    echo 'Oops! the name of the database should be between 4 to 15 characters long. Only use alpha numeric characters'
    echo 
    read -p 'Enter the name of the database once again' MONGODB_HOSTNAME
done
if [[ $MONGODB_HOSTNAME = "" ]]; then 
    echo MONGODB_HOSTNAME=mongodb | tee -a .env #$LOCAL_APP_PATH/.env
else 
    echo MONGODB_HOSTNAME=$MONGODB_HOSTNAME | tee -a .env #$LOCAL_APP_PATH/.env
fi 




DOCKER_HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
echo DOCKER_HOST=$DOCKER_HOST >> $LOCAL_APP_PATH/.env

echo LOCAL_APP_PATH=$LOCAL_APP_PATH >> .env
echo DESTINATION_APP=$DESTINATION_APP | tee -a .env 



