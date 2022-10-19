# -*- encoding: utf-8 -*-

# all the imports necessary
from flask import (
    url_for,
    redirect,
    render_template,
    request,
    current_app,
    Blueprint,
)

# from app import lm, bc
from flask_login import login_user, logout_user
from audacious_webui.models.users import Users
from audacious_webui.forms import LoginForm, SignupForm
import logging
from werkzeug.security import check_password_hash, generate_password_hash


LOGGER = logging.getLogger(__name__)

auth = Blueprint("auth", __name__)


# authenticate user
@auth.route("/logout.html")
def logout():
    logout_user()
    return redirect(url_for("home.homepage"))


# register user
@auth.route("/signup.html", methods=["GET", "POST"])
def signup():

    # define login form here
    form = SignupForm(request.form)

    msg = None
    success = False

    # custommize your pate title / description here
    page_title = "Sign up"
    # page_description = 'User registration page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get("username", "", type=str)
        password = request.form.get("password", "", type=str)
        name = request.form.get("name", "", type=str)
        email = request.form.get("email", "", type=str)

        # filter User out of database through username
        user = current_app.session.query(Users).filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = current_app.session.query(Users).filter_by(email=email).first()

        if user or user_by_email:
            msg = "Error: User exists!"

        else:
            pw_hash = generate_password_hash(password)
            user = Users(username, pw_hash, name, email)
            user.save(current_app.session)

            success = True
            msg = f"""<div class="notification is-success container">
                        <button class="delete"></button>
                        User created, please
                        <a href={url_for('auth.login')}>login</a>
                      </div>"""

    return render_template(
        "layouts/default.html",
        title=page_title,
        content=render_template(
            "pages/signup.html", form=form, msg=msg, success=success
        ),
    )


# authenticate user
@auth.route("/login.html", methods=["GET", "POST"])
def login():

    # define login form here
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # custommize your page title / description here
    page_title = "Login"
    # page_description = 'Login page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get("username", "", type=str)
        password = request.form.get("password", "", type=str)

        # filter User out of database through username
        user = current_app.session.query(Users).filter_by(user=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("home.homepage"))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template(
        "layouts/default.html",
        title=page_title,
        content=render_template("pages/login.html", form=form, msg=msg),
    )


# error handling
# most common error codes have been added for now
# TO DO:
# they could use some styling so they don't look so ugly


def http_err(err_code):

    err_msg = "Oups !! Some internal error ocurred. Thanks to contact support."

    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:
        err_msg = "The URL you were looking for does not seem to exist."

    elif 500 == err_code:
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg


@auth.errorhandler(401)
def e401(e):
    return http_err(401)  # not allowed


@auth.errorhandler(404)
def e404(e):
    return http_err(404)  # does not exist


@auth.errorhandler(500)
def e500(e):
    return http_err(500)  # internal error


@auth.errorhandler(403)
def e403(e):
    return http_err(403)  # forbidden access


@auth.errorhandler(410)
def e410(e):
    return http_err(410)  # deleted content
