import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

allow_url = {
    "production": {
        "POST": [
            "https://nrank.api.sellertool.io/api/v1/nrank-record-details/results"
        ]

        # Docker Setting
    },
    "development": {
        "POST": [
            "http://localhost:23081/api/v1/nrank-record-details/results"
        ]
    }
}

url = allow_url[os.environ.get('FLASK_ENV')]

class WhitelistUrlUtils():
    
    @staticmethod    
    def get_csrf_whitelist_url():
        return url
    