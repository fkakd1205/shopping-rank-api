# from flask_sqlalchemy import SQLAlchemy

# from config.db.DatabaseConfig import db_url

# db = SQLAlchemy()

# def close_db(e=None):
#     db.session.close()
#     db.session.remove()

# def init_app(app):

#     app.teardown_appcontext(close_db)

#     app.config["SQLALCHEMY_DATABASE_URI"] = db_url
#     app.config['SQLALCHEMY_ECHO'] = True        # sql log
    
#     # 다음 설정 deprecated 
#     # app.config['SQLALCHEMY_POOL_SIZE'] = 5
#     # app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
#     # app.config['SQLALCHEMY_POOL_RECYCLE'] = 30
#     db.init_app(app)
