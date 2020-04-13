#!/bin/sh
#
echo "Preparing folder init and creating ./init/initdb.sql"
mkdir ./init >/dev/null 2>&1
chmod -R +x ./init
docker run --rm guacamole/guacamole:1.0.0 /opt/guacamole/bin/initdb.sh --postgres > ./init/initdb.sql
echo "done"