#!/bin/bash
docker-compose up -d
python3 ./vagrant/vagrant_server/src/VagrantServer.py
