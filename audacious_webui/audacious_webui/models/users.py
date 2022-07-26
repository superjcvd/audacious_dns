# -*- encoding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from audacious_webui.common import DATATYPE
from audacious_webui.database import db


class Users(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    user = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    name = Column(String(500))
    role = Column(Integer)
    password = Column(String(500))
    password_q = Column(Integer)

    def __init__(self, user, password, name, email):
        self.user = user
        self.password = password
        self.password_q = DATATYPE.CRYPTED
        self.name = name
        self.email = email

        self.group_id = None
        self.role = None

    def __repr__(self):
        return f"<User ({self.id})>"

    def save(self):
        # inject self into db session
        db.session.add(self)
        # commit change and save the object
        db.session.commit()
        return self
