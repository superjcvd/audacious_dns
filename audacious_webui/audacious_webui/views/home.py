# -*- encoding: utf-8 -*-
import os
import logging
from flask import render_template, Blueprint, send_from_directory
from werkzeug.exceptions import abort

LOGGER = logging.getLogger(__name__)

LOGGER.info(__name__)
home = Blueprint("home", __name__)


# App main route + generic routing
@home.route("/", defaults={"path": "home.html"})
@home.route("/<path>")
def homepage(path):
    try:
        return render_template(
            "layouts/default.html", content=render_template("pages/" + path)
        )
    except Exception as e:
        LOGGER.error(e)
        abort(404)


@home.route("/favicon.ico")
def favicon():
    # return send_from_directory(os.path.join(app.root_path, 'static'),
    #                             'favicon.ico', mimetype='image/vnd.microsoft.icon')
    return send_from_directory(
        "./app/static/img/", "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@home.route("/sitemap.xml")
def sitemap():
    return send_from_directory("/static/sitemap.xml")
