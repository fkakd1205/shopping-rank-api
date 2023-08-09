from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.key.db.DatabaseConfig import db_url

engine = create_engine(url=db_url, pool_size=1, max_overflow=2, pool_recycle=3600, pool_timeout=30)
# engine = create_engine(url=db_url, echo=True, pool_size=1, max_overflow=2, pool_recycle=3600, pool_timeout=30)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_session = Session()

Base = declarative_base()

def close_db(e=None):
    db_session.close()

def init_db(app):
    app.teardown_appcontext(close_db)
