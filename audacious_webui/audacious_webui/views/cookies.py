from flask import Blueprint, request, current_app, render_template, redirect, url_for
from markupsafe import escape
from audacious_webui.models.cookies import Cookies
from werkzeug.exceptions import abort
import logging

LOGGER = logging.getLogger(__name__)

cookies = Blueprint('cookies', __name__, url_prefix='/cookies')

@cookies.route('/view', methods=['GET'])
def cookies_view():
    with current_app.app_context():
        cookies = current_app.session.query(Cookies).all()

    return render_template(
            "layouts/default.html",
            content=render_template(
                'pages/cookies.html', 
                cookies=cookies
            )
    )


@cookies.route('/add', methods=['GET', 'POST'])
def cookies_add():

    if request.method == 'POST':
        args = request.form
    
    if request.method == 'GET':
        args = request.args

    ip = args.get('ip', type=str) or ""
    cookies = args.get('cookies', type=str) or ""

    new_cookies = Cookies(ip=ip, cookies=cookies)
    new_cookies.db_add_cookies(current_app.session)

    return f"{ip} --> {cookies}"


@cookies.route('/delete', methods=['GET', 'POST'])
def cookies_delete():
    try:
        if request.method == "POST":
            cookies_id = request.form["id"]
            LOGGER.error(f"DELETE --> cookies id {id}")
            Cookies.db_delete_cookies(current_app.session, cookies_id)

            return redirect(url_for("cookies.cookies_view"))
        else:
            return "ok"
    except Exception as e:
        LOGGER.error(e)
        abort(404)