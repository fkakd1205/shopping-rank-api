from flask import g
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.environment.CustomLoadDotEnv import custom_load_dotenv

from config.db.DatabaseConfig import db_url, slave_db_url

custom_load_dotenv()

pool_size = int(os.environ.get('POOL_SIZE'))
max_overflow = int(os.environ.get('MAX_OVERFLOW'))
pool_recycle = int(os.environ.get('POOL_RECYCLE'))
pool_timeout = int(os.environ.get('POOL_TIMEOUT'))

engine = create_engine(url=db_url, pool_size=pool_size, max_overflow=max_overflow, pool_recycle=pool_recycle, pool_timeout=pool_timeout)

# TODO :: isolation level 설정
slave_engine = create_engine(url=slave_db_url, pool_size=pool_size, max_overflow=max_overflow, pool_recycle=pool_recycle, pool_timeout=pool_timeout)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
slave_db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=slave_engine))    

Base = declarative_base()

def close_db(e=None):
    db_session.close()
    db_session.remove()

    slave_db_session.close()
    slave_db_session.remove()

def init_db(app):
    app.teardown_appcontext(close_db)

def get_db_session():
    is_read_only = g.get('read_only', False)
    return slave_db_session if is_read_only else db_session
