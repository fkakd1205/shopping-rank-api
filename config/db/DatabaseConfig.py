import os
from dotenv import load_dotenv

from config.pycryptodome.PyCryptoDomeConfigSetting import PyCryptoDomeConfigSetting

load_dotenv()

pwd = os.environ.get('ENC_PASSWORD')
configSetting = PyCryptoDomeConfigSetting(pwd)

db_adapter = "pymysql"

user = configSetting.decrypt(os.environ.get('DB_USER'))
password = configSetting.decrypt(os.environ.get('DB_PASSWORD'))
host = configSetting.decrypt(os.environ.get('DB_HOST'))
port = os.environ.get('DB_PORT')
database = configSetting.decrypt(os.environ.get('DB_DATABASE'))

db_url = f"mysql+{db_adapter}://{user}:{password}@{host}:{port}/{database}"
