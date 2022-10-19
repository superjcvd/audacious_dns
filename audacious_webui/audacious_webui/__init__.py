# -*- encoding: utf-8 -*-
from flask import Flask, current_app
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import logging
import os
import subprocess
import queue
import threading
from flask_socketio import SocketIO
from flask_socketio import send, emit

# from flask_bootstrap  import Bootstrap
# from flask_mail import Mail

from audacious_webui.configuration import get_config


from audacious_webui.models.users import Users
from audacious_webui.models.domains import Domains
from audacious_webui.models.statistics import Statistics
from audacious_webui.models.base import Base
from audacious_webui.views.home import home
from audacious_webui.views.auth import auth
from audacious_webui.views.cookies import cookies
from audacious_webui.views.domains import domains
from audacious_webui.views.statistics import statistics
from audacious_webui.views.terminal import terminal
# from audacious_webui.database import db
from audacious_webui.database import MySession, engine


# logging.basicConfig(level=logging.INFO)
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)
LOGGER = logging.getLogger(__name__)

q = queue.Queue()
lm = LoginManager()
bc = Bcrypt()
# mg = Migrate()
# mail = Mail()
# bootstrap = Bootstrap()
# moment = Moment()
# babel = Babel()

# LOGGER.debug("Loading the following models:")
# LOGGER.debug(modelsUsers)
# LOGGER.debug(Domains)
# LOGGER.debug(Statistics)


def create_app():
    conf = get_config()
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(conf)
    socketio = SocketIO(app)
    # app.add_template_global(app.config, "cfg")

    lm.init_app(app)
    # mg.init_app(app, db)
    # mail.init_app(app)
    # bootstrap.init_app(app)
    # moment.init_app(app)
    # babel.init_app(app)

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(cookies)
    app.register_blueprint(domains)
    app.register_blueprint(statistics)
    app.register_blueprint(terminal)

    @socketio.on('client_event')
    def handle_client_event(client_data: dict):
        print('receive json: ' + str(client_data) )
        q.put_nowait(client_data['data'])

    with app.app_context():
        Base.metadata.create_all(bind=engine)
        app.session = MySession() # register a session param in the app
        # db.create_all()
        background_bash(socketio)


    @app.after_request
    def apply_security(response):
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

    # provide login manager with load_user callback
    @lm.user_loader
    def load_user(user_id):
        return current_app.session.query(Users).get(int(user_id))

    return app



def background_bash(socketio: SocketIO):
    global q
    command = 'bash'
    def stdout_reader(p: subprocess.Popen, socketio):
        for line in p.stdout:
            server_data = line.rstrip()
            socketio.emit('server_response', server_data)
    def stdin_writer(p, q):
        try: 
            while True:
                data = q.get()
                p.stdin.write((data + "\n"))
                p.stdin.flush()
                q.task_done()
        finally:
            p.stdin.close()
    try:
        p = subprocess.Popen(command,
                preexec_fn=os.setsid,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True)
        
        t_output = threading.Thread(target=stdout_reader, args=(p, socketio), daemon=True)
        t_output.start()

        t_input = threading.Thread(target=stdin_writer, args=(p, q), daemon=True)
        t_input.start()
    finally:
        print("bash started...")


if __name__ == "__main__":
    LOGGER.info("")
