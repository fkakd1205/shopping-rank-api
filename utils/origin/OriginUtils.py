import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

allow_origins = {
    "production": [
        "https://v2.sellertool.io",
        "https://api.sellertool.io",
        "https://scp.sellertool.io",
        "https://auth.api.sellertool.io",
        "https://api.sellertool.io/wsc",
        "https://sales-analysis.sellertool.io",
        "https://nrank.api.sellertool.io"
    ],
    "development": [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8181",
        "http://localhost:5000",
        "http://localhost:23081"
    ]
}

origins = allow_origins[os.environ.get('FLASK_ENV')]

class OriginUtils():
    
    @staticmethod    
    def get_white_list_origins():
        return origins