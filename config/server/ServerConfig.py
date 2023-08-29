import os
from dotenv import load_dotenv

load_dotenv()

development_config = {
    "origin": {
        "auth-api": "http://localhost:9081",
        "store-rank-api": "http://localhost:5000"
    }
}

production_config = {
    "origin": {
        "auth-api": "https://auth.api.sellertool.io",
        "store-rank-api": "https://nrank.api.sellertool.io"
    }
}

app_config = {
    'development': development_config,
    'production': production_config
}

config = app_config[os.environ.get('FLASK_ENV')]
