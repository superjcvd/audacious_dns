#!/usr/bin/env python

from distutils.core import setup


setup(
    name="audacious_webui",
    description="Webui for DNS filtering",
    url="https://github.com/",
    author="Gaël Soudé",
    author_email="gael.soude@gmail.com",
    packages=[
        "audacious_webui",
        "audacious_webui.models",
        "audacious_webui.views",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-login",
        "flask-bcrypt",
        "flask-migrate",
        "flask-wtf",
        "email_validator",
        "alembic",
        "waitress",
    ],
)
