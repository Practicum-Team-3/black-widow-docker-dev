# settings.py will take care of creating .env file. The .env file will help set variables dynamically in the system.
from dotenv import load_dotenv
import os

load_dotenv()

env_debug = os.getenv("ENVIRONMENT_DEBUG")
widow_app_ip = os.getenv("WIDOW_IP")
widow_app_port = os.getenv("BW_APP_PORT")
environment_debug= os.getenv("ENVIRONMENT_DEBUG")

vagrant_host_ip = os.getenv("DOCKER_HOST")
#THIS SHOULD CHANGE TO VAGR_APP_PORT TO BE DONE LATER
vagrant_app_port = os.getenv("BW_APP_PORT")

mongodb_hostname = os.getenv("MONGODB_HOSTNAME")
db_name = os.getenv("MONGODB_DATABASE")
mongodb_username = os.getenv("MONGODB_USERNAME")
mongdb_password = os.getenv("MONGODB_PASSWORD")
mongodb_ip = os.getenv("MONGODB_IP")
mongodb_port = os.getenv("MONGODB_PORT")
mongodb_root_username = os.getenv("MONGODB_ROOT_USER")
mongodb_root_password = os.getenv("MONGODB_ROOT_PASSWORD")