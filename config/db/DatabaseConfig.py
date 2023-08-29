import os
from dotenv import load_dotenv

from utils.pycryptodome.PyCryptoDomeUtils import PyCryptoDomeUtils

load_dotenv()

pwd = os.environ.get('ENC_PASSWORD')
cryptoDomeUtils = PyCryptoDomeUtils(pwd)

db_adapter = "pymysql"

user = cryptoDomeUtils.decrypt(os.environ.get('DB_USER'))
password = cryptoDomeUtils.decrypt(os.environ.get('DB_PASSWORD'))
host = cryptoDomeUtils.decrypt(os.environ.get('DB_HOST'))
port = os.environ.get('DB_PORT')
database = cryptoDomeUtils.decrypt(os.environ.get('DB_DATABASE'))

db_url = f"mysql+{db_adapter}://{user}:{password}@{host}:{port}/{database}"
