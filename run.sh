#!/bin/bash
docker-compose up -d
cd ./vagrant/vagrant_server/src/
python3 VagrantServer.py
