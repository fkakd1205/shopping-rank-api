import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

allow_path = {
    "production": {
        "POST": [
            "/api/v1/nrank-record-details/for:nrankSearchModal/action:save"
        ]
    },
    "development": {
        "POST": [
            "/api/v1/nrank-record-details/for:nrankSearchModal/action:save"
        ]
    }
}

path = allow_path[os.environ.get('FLASK_ENV')]

class WhitelistPathUtils():
    
    @staticmethod    
    def get_csrf_whitelist_path():
        return path
    