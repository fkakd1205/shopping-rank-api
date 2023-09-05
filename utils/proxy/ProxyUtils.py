import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

class ProxyUtils():
    PROXY_REQUEST_URL = os.environ.get('SMART_PROXY_REQUEST_URL')