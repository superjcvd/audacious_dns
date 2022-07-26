# -*- encoding: utf-8 -*-
import os

# Grabs the folder where the script runs.
BASEDIR = os.path.abspath(os.path.dirname(__file__))
BD_PATH_DEV = "database/database.db"
BD_PATH_PROD = "/var/audacious_dns/database/database.db"


class AppConfig(object):

    # THEME = 'phantom'

    STATIC = "static"
    DATE_FORMAT = "%Y-%m-%d"
    SECRET_KEY = "SecretKey_666***!"  # save yours here


class Config(AppConfig):
    """
    Configuration base, for all environments.
    """

    DEBUG = False
    TESTING = False
    BOOTSTRAP_FONTAWESOME = True
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):

    APP = "audacious_webui"
    APP_IMG_FOLDER = os.path.join(APP, "static", "images")

    # RECAPTCHA keys (production)
    RECAPTCHA_PUBLIC_KEY = "1234_abcd"
    RECAPTCHA_PRIVATE_KEY = "1234_xyzw"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, BD_PATH_PROD)}"
    # mysql+pymysql://db_user:db_pass@localhost/db_name

    # SERVER_NAME = "audacious-unicorn.com"
    SERVER_NAME = "127.0.0.1:8080"
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):

    APP = "audacious_webui"
    APP_IMG_FOLDER = os.path.join(APP, "static", "images")

    # keys for dev [ http://localhost ]
    RECAPTCHA_PUBLIC_KEY = "1234_abcd"
    RECAPTCHA_PRIVATE_KEY = "1234_xyzw"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, BD_PATH_DEV)}"

    # SERVER_NAME = "audacious-unicorn.com:5000"
    SERVER_NAME = "127.0.0.1:5000"
    DEBUG = False
    TESTING = False
    FORCE_HTTPS = False
