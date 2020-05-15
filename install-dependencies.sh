#!/bin/bash
echo 'Installing Celery dependencies'
sudo apt-get install -y tcl


echo 'Installing Celery dependencies'
# Installing Saltstack on Hostmachine
wget -O - https://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -

echo "deb http://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest bionic main" >> /etc/apt/sources.list.d/saltstack.list
apt-get update
sudo apt-get install salt-master




