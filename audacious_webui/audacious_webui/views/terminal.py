from flask import Blueprint, request, current_app, render_template, redirect, url_for
from markupsafe import escape
from werkzeug.exceptions import abort
import logging

LOGGER = logging.getLogger(__name__)

terminal = Blueprint('terminal', __name__, url_prefix='/terminal')

@terminal.route('/', methods=['GET'])
def terminal_view():

    return render_template(
            "layouts/default.html",
            content=render_template(
                'pages/terminal.html'
            )
    )