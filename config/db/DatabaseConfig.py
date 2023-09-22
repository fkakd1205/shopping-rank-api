import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

from config.pycryptodome.AES128Crypto import AES128Crypto

custom_load_dotenv()

pwd = os.environ.get('ENC_PASSWORD')
configSetting = AES128Crypto(pwd)

db_adapter = "pymysql"
slave_db_adapter = "pymysql"

user = configSetting.decrypt(os.environ.get('DB_USER'))
slave_user = configSetting.decrypt(os.environ.get('SLAVE_DB_USER'))

password = configSetting.decrypt(os.environ.get('DB_PASSWORD'))
slave_password = configSetting.decrypt(os.environ.get('SLAVE_DB_PASSWORD'))

host = configSetting.decrypt(os.environ.get('DB_HOST'))
slave_host = configSetting.decrypt(os.environ.get('SLAVE_DB_HOST'))

port = os.environ.get('DB_PORT')
slave_port = os.environ.get('SLAVE_DB_PORT')

database = configSetting.decrypt(os.environ.get('DB_DATABASE'))
slave_database = configSetting.decrypt(os.environ.get('SLAVE_DB_DATABASE'))

db_url = f"mysql+{db_adapter}://{user}:{password}@{host}:{port}/{database}"
slave_db_url = f"mysql+{slave_db_adapter}://{slave_user}:{slave_password}@{slave_host}:{slave_port}/{slave_database}"
