# -*- encoding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import logging
import os

# from flask_bootstrap  import Bootstrap
# from flask_mail import Mail
from audacious_webui.models.users import Users
from audacious_webui.models.domains import Domains
from audacious_webui.models.statistics import Statistics
from audacious_webui.views.home import home
from audacious_webui.views.auth import auth
from audacious_webui.views.domains import domains
from audacious_webui.views.statistics import statistics
from audacious_webui.database import db


# logging.basicConfig(level=logging.INFO)
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)
LOGGER = logging.getLogger(__name__)

lm = LoginManager()
bc = Bcrypt()
mg = Migrate()
# mail = Mail()
# bootstrap = Bootstrap()
# moment = Moment()
# babel = Babel()

LOGGER.debug("Loading the following models:")
LOGGER.debug(Users)
LOGGER.debug(Domains)
LOGGER.debug(Statistics)


if os.environ.get('FLASK_CONFIG') == 'development':
    config_name = "audacious_webui.configuration.DevelopmentConfig"
else:
    config_name = "audacious_webui.configuration.ProductionConfig"


def create_app(config_class=config_name):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)
    app.add_template_global(app.config, "cfg")

    db.init_app(app)
    lm.init_app(app)
    mg.init_app(app, db)
    # mail.init_app(app)
    # bootstrap.init_app(app)
    # moment.init_app(app)
    # babel.init_app(app)

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(domains)
    app.register_blueprint(statistics)

    with app.app_context():
        db.create_all()

    @app.after_request
    def apply_security(response):
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

    # provide login manager with load_user callback
    @lm.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app


if __name__ == "__main__":
    LOGGER.info("")
