import os
from config.environment.CustomLoadDotEnv import custom_load_dotenv

custom_load_dotenv()

nrankDirectAccessKey = os.environ.get('NRANK_DIRECT_ACCESS_KEY')

development_config = {
    "origin": {
        "auth-api": "http://localhost:9081",
        "store-rank-api": "http://localhost:23081"
    },
    "nrankDirectAccessKey": nrankDirectAccessKey,
}

production_config = {
    "origin": {
        "auth-api": "https://auth.api.sellertool.io",
        "store-rank-api": "https://nrank.api.sellertool.io"

        # Docker Setting
        # "auth-api": "http://host.docker.internal:9081",
        # "store-rank-api": "http://host.docker.internal:23081"
    },
    "nrankDirectAccessKey": nrankDirectAccessKey,
}

app_config = {
    'development': development_config,
    'production': production_config
}

config = app_config[os.environ.get('FLASK_ENV')]
