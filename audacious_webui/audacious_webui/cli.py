# -*- encoding: utf-8 -*-
import re
from flask_frozen import Freezer
from audacious_webui import bc, create_app
from audacious_webui.models.users import Users
from audacious_webui.models.domains import Domains


# in order to work outside the flask app
app = create_app()
app.app_context().push()


def export_static():
    freezer = Freezer(app)
    freezer.freeze()


def create_user(email, name, username, password):

    # regex to check for e-mail syntax
    if not re.match("(^.+@{1}.+.{1}.+)", str(email)):
        print("Invalid e-mail. Please try again.")
        return None
        # return "Invalid e-mail. Please try again."
    # hash the password here (bcrypt has salting included)
    pw_hash = bc.generate_password_hash(password)
    user = Users(username, pw_hash, name, email)
    user.save()

    print("user created ok: " + str(user.id))
    return user


def create_domain(domain_name, domain_type, domain_isactive):
    domain = Domains(domain_name, domain_type, domain_isactive)
    domain.db_domains_add()
    print(f"Domain '{domain.domain_id}' created")
    return domain
