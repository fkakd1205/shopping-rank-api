import os

allow_origins = {
    "production": [
        # "https://www.sellertool.io",
        # "https://api.sellertool.io",
        # "https://www.sellertl.com",
        # "https://api.sellertl.com",
        # "https://nrank.sellertl.com",

        # TODO :: 제거
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8181"
        "http://localhost:5000",    # TODO :: 제거
        "http://localhost:23081"
    ],
    "development": [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8181",
        "http://localhost:5000",    # TODO :: 제거
        "http://localhost:23081"
    ]
}

origins = allow_origins[os.environ.get('FLASK_ENV')]

class OriginUtils():
    
    @staticmethod    
    def get_white_list_origins():
        return origins