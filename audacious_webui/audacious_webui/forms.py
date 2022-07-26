# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SelectField,
    validators,
    SubmitField,
)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.InputRequired()])
    password = PasswordField("Password", validators=[validators.InputRequired()])


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[validators.InputRequired()])
    password = PasswordField("Password", validators=[validators.InputRequired()])
    email = StringField(
        "Email", validators=[validators.InputRequired(), validators.Email()]
    )
    name = StringField("Name", validators=[validators.InputRequired()])


class DomainsForm(FlaskForm):
    # domain_id = StringField(u"ID")
    domain_name = StringField(
        "Domain", validators=[validators.InputRequired(message="no domain specified")]
    )
    domain_type = StringField(
        "Type", validators=[validators.InputRequired(message="no type specified")]
    )
    # domain_isactive = SelectField(u"Active", choices=[('True', 'Yes'), ('False', 'No')], validators=[validators.InputRequired()])
    # domain_isactive = BooleanField(u"Active", default=True)
    domain_isactive = BooleanField("Active")

    domain_add = SubmitField(label=("Add"))
    domain_edit = SubmitField(label=("Edit"))
