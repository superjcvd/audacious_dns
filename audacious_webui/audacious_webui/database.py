# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask

# db = SQLAlchemy()


# def import_database():
#     app = Flask(__name__)
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app/database/database_dev.db"
#     db = SQLAlchemy(app)
#     return db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from audacious_webui.configuration import get_config

conf = get_config()
engine = create_engine(conf.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
MySession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))