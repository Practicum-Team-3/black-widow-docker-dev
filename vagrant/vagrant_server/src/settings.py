# settings.py will take care of creating .env file. The .env file will help set variables dynamically in the system.
from dotenv import load_dotenv
import os

load_dotenv()

env_debug = os.getenv("ENVIRONMENT_DEBUG")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

mongodb_ip = os.getenv("MONGODB_IP")
mongodb_port = os.getenv("MONGODB_PORT")
mongodb_root_username = os.getenv("MONGODB_ROOT_USER")
mongodb_root_password = os.getenv("MONGODB_ROOT_PASSWORD")