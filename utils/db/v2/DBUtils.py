from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.db.DatabaseConfig import db_url

engine = create_engine(url=db_url, pool_size=1, max_overflow=3, pool_recycle=3600, pool_timeout=30)
# engine = create_engine(url=db_url, echo=True, pool_size=1, max_overflow=2, pool_recycle=3600, pool_timeout=30)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def close_db(e=None):
    db_session.close()
    db_session.remove()

def init_db(app):
    app.teardown_appcontext(close_db)
