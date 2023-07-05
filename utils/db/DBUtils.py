from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

from config.db.DatabaseConfig import db_url

db = SQLAlchemy()

Base = db.Model

def get_session() -> Session:
    return db.session

def close_db(e=None):
    db.session.close()

def init_app(app):
    app.teardown_appcontext(close_db)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    db.init_app(app)