import os
from dotenv import load_dotenv

load_dotenv()

def custom_load_dotenv():
    env = os.environ.get('FLASK_ENV')

    if(env == 'development'):
        load_dotenv('.env.dev')
    elif(env == 'production'):
        load_dotenv('.env.prod')
