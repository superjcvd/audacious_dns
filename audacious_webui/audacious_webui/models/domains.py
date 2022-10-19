
from flask import Flask, flash
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Unicode, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from audacious_webui.models.base import Base
import re
import logging
# from audacious_webui.database import db

LOGGER = logging.getLogger(__name__)


class Domains(Base):
    __tablename__ = "domains"
    domain_id = Column(Integer, primary_key=True)
    domain_name = Column(Unicode(65), nullable=False, index=True, unique=True)
    domain_type = Column(Unicode(50), nullable=False)
    domain_isactive = Column(Boolean, default=True)
    domain_stats = relationship(
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

    def db_domains_add(self, session):
        try:
            session.add(self)
            session.commit()
            return self
        except IntegrityError:
            flash("Duplicate entry!")
            return None
            pass

    def db_domains_get_all(session):
        return session.query(Domains).all()

    def db_domains_get_paginate(session, page_number, max_per_page):
        num_domains = int(session.query(Domains).count())
        domains = (
            session.query(Domains)
            .offset((page_number - 1) * max_per_page)
            .limit(max_per_page)
            .all()
        )
        return num_domains, domains

    def db_domains_get_by_name(session, domain_name):
        return session.query(Domains).filter_by(domain_name=domain_name).first()

    def db_domains_get_by_id(session, domain_id):
        return session.query(Domains).get(domain_id)

    @classmethod
    def db_domains_update(cls, session, domain_id, domain_dict):
        try:
            # if 'domain_name' in domain_dict and not cls.validate_domain_name(domain_dict['domain_name']):
            #     raise ValueError("not a domain!")
            # if 'domain_type' in domain_dict and not cls.validate_domain_type(domain_dict['domain_type']):
            #     raise ValueError("not a valid domain type!")

            session.query(Domains).filter_by(domain_id=domain_id).update(domain_dict)
            session.commit()

        except ValueError as e:
            LOGGER.error(e)
            pass
        except IntegrityError:
            LOGGER.error("Duplicate entry?")
            pass

    @classmethod
    def db_domains_delete_by_id(cls, session, domain_id):
        domain_to_delete = session.query(Domains).get(domain_id)
        session.delete(domain_to_delete)
        session.commit()

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

    # session.close()


if __name__ == "__main__":
    main()
