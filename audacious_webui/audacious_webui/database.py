from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def import_database():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app/database/database_dev.db"
    db = SQLAlchemy(app)
    return db
