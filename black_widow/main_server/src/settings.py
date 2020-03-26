# settings.py will take care of creating .env file. The .env file will help set variables dynamically in the system.
from dotenv import load_dotenv
import os

load_dotenv()

vagrant_host_ip = os.getenv("DOCKER_HOST")
#THIS SHOULD CHANGE TO VAGR_APP_PORT TO BE DONE LATER
vagrant_app_port = os.getenv("BW_APP_PORT")
