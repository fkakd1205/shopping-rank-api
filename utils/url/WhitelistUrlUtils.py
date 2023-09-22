import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

allow_url = {
    "production": {
        "GET": [],
        "POST": [
            "https://nrank.api.sellertool.io/api/v1/nrank-record-details/results"
        ],
        "PATCH": []

        # Docker Setting
    },
    "development": {
        "GET": [],
        "POST": [
            "http://localhost:23081/api/v1/nrank-record-details/results"
        ],
        "PATCH": []
    }
}

url = allow_url[os.environ.get('FLASK_ENV')]

class WhitelistUrlUtils():
    
    @staticmethod    
    def get_csrf_whitelist_url():
        return url
    