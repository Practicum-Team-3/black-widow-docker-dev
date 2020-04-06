# settings.py will take care of creating .env file. The .env file will help set variables dynamically in the system.
from dotenv import load_dotenv
import os

load_dotenv()

class ConfigManager():
    def __init__(self):
        self.env_debug = os.getenv("ENVIRONMENT_DEBUG")
        #Widow server conf
        self.widow_app_ip = os.getenv("WIDOW_IP")
        self.widow_app_port = os.getenv("BW_CON_PORT")
        #Vagrant server conf
        self.vagrant_host_ip = os.getenv("DOCKER_HOST")
        self.vagrant_app_port = os.getenv("BW_APP_PORT")
        #Upload conf
        self.upload_ip = '172.18.128.4'
        self.upload_port = '5000'
        #Redis conf
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_port = os.getenv("REDIS_PORT")
        #Mongodb conf
        self.mongodb_ip = os.getenv("MONGODB_IP")
        self.mongodb_port = os.getenv("MONGODB_PORT")
        self.mongodb_root_username = os.getenv("MONGODB_ROOT_USER")
        self.mongodb_root_password = os.getenv("MONGODB_ROOT_PASSWORD")

    def vagrantURL(self):
        vagrant_url = "http://" + self.vagrant_host_ip + ":" + self.vagrant_app_port
        return vagrant_url

    def mongoURL(self):
        mongodb_url = "mongodb://" + self.mongodb_root_username + ":" + self.mongodb_root_password + "@" + self.mongodb_ip + ":" + self.mongodb_port
        return mongodb_url

    def uploadURL(self):
        upload_url = 'http://' + self.upload_ip + ':' + self.upload_port
        return upload_url

    def redisURL(self):
        redis_url = 'redis://' + self.redis_host + ':' + self.redis_port + '/0'
        return redis_url



