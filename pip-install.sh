VAGRANT_SERVER=./vagrant/vagrant_server/src/
VAGRANT_REQUIREMENTS=../../requirements.txt
cd $VAGRANT_SERVER
pip3 install -r $VAGRANT_REQUIREMENTS
pip3 install -U "celery[redis]"

