# from app.views.domains import LOGGER
from sqlalchemy.exc import IntegrityError
from flask import Flask, flash
import re
import logging
from audacious_webui.database import db

LOGGER = logging.getLogger(__name__)


class Domains(db.Model):
    __tablename__ = "domains"
    domain_id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.Unicode(65), nullable=False, index=True, unique=True)
    domain_type = db.Column(db.Unicode(50), nullable=False)
    domain_isactive = db.Column(db.Boolean, default=True)
    domain_stats = db.relationship(
        "Statistics", backref="domains", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"""<Domains (
                    domain_id={self.domain_id},
                    domain_name={self.domain_name},
                    domain_type={self.domain_type},
                    domain_isactive={str(self.domain_isactive)}
                    domain_stats={self.domain_stats}
                )>"""

    def __init__(
        self, domain_name: str, domain_type: str, domain_isactive: bool = True
    ):
        if not self.validate_domain_name(domain_name):
            raise ValueError("not a domain!")
        if not self.validate_domain_type(domain_type):
            raise ValueError("not a valid domain type!")

        self.domain_name = str(domain_name)
        self.domain_type = str(domain_type)
        self.domain_isactive = bool(domain_isactive)

    def db_domains_add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            flash("Duplicate entry!")
            return None
            pass

    def db_domains_get_all():
        return db.session.query(Domains).all()

    def db_domains_get_paginate(page_number, max_per_page):
        num_domains = int(db.session.query(Domains).count())
        domains = (
            db.session.query(Domains)
            .offset((page_number - 1) * max_per_page)
            .limit(max_per_page)
            .all()
        )
        return num_domains, domains

    def db_domains_get_by_name(domain_name):
        return db.session.query(Domains).filter_by(domain_name=domain_name).first()

    def db_domains_get_by_id(domain_id):
        return db.session.query(Domains).get(domain_id)

    @classmethod
    def db_domains_update(cls, domain_id, domain_dict):
        try:
            # if 'domain_name' in domain_dict and not cls.validate_domain_name(domain_dict['domain_name']):
            #     raise ValueError("not a domain!")
            # if 'domain_type' in domain_dict and not cls.validate_domain_type(domain_dict['domain_type']):
            #     raise ValueError("not a valid domain type!")

            db.session.query(Domains).filter_by(domain_id=domain_id).update(domain_dict)
            db.session.commit()

        except ValueError as e:
            LOGGER.error(e)
            pass
        except IntegrityError:
            LOGGER.error("Duplicate entry?")
            pass

    @classmethod
    def db_domains_delete_by_id(cls, domain_id):
        domain_to_delete = db.session.query(Domains).get(domain_id)
        db.session.delete(domain_to_delete)
        db.session.commit()

    @staticmethod
    def validate_domain_name(domain_name):
        pattern = re.compile("^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$")
        if pattern.match(domain_name):
            return True
        else:
            return False

    @staticmethod
    def validate_domain_type(domain_type):
        pattern = re.compile("^[a-zA-Z0-9-]{1,50}$")
        if pattern.match(domain_type):
            return True
        else:
            return False


def main():

    # test1 = Domains('crouteo.com', 'ads', 1)
    # Domains.db_domains_update(1,test1)

    print(Domains.db_domains_get_all())

    db.session.close()


if __name__ == "__main__":
    main()
