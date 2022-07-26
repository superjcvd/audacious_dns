# -*- encoding: utf-8 -*-

from flask import json
from audacious_webui import app
from audacious_webui import db

# build a Json response
def response(data):
    return app.response_class(
        response=json.dumps(data), status=200, mimetype="application/json"
    )


def g_db_commit():

    db.session.commit()


def g_db_add(obj):

    if obj:
        db.session.add(obj)


def g_db_del(obj):

    if obj:
        db.session.delete(obj)
