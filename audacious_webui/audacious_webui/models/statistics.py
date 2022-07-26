from sqlalchemy.exc import IntegrityError
from flask import flash
import logging

from audacious_webui.database import db
from audacious_webui.models.domains import Domains

LOGGER = logging.getLogger(__name__)


class Statistics(db.Model):
    __tablename__ = "statistics"
    __table_args__ = (
        db.UniqueConstraint(
            "stats_domain_id", "stats_client_ip", name="couple_ip_domain"
        ),
    )
    stats_id = db.Column(db.Unicode(128), primary_key=True)
    stats_domain_id = db.Column(
        db.Integer, db.ForeignKey("domains.domain_id"), nullable=False
    )
    stats_client_ip = db.Column(db.Unicode(45))
    stats_request_count = db.Column(db.Integer)

    def __repr__(self):
        return f"""<Statistics (
                    stats_id={self.stats_id},
                    stats_domain_id={self.stats_domain_id},
                    stats_client_ip={self.stats_client_ip},
                    stats_request_count={self.stats_request_count}
                )>"""

    def __init__(self, stats_domain_id, stats_client_ip):
        self.stats_domain_id = stats_domain_id
        self.stats_client_ip = stats_client_ip
        self.stats_request_count = 0

    def db_init():
        # Base.metadata.create_all()
        db.create_all()

    def db_update():
        pass  # something with alembic

    def db_delete():
        # Base.metadata.drop_all()
        db.drop_all()

    def db_statistics_add(database_object):
        try:
            db.session.add(database_object)
            db.session.commit()
        except IntegrityError:
            flash("Duplicate entry!")
            pass

    def db_statistics_get_paginate(page_number, max_per_page):
        num_statistics = int(db.session.query(Statistics).count())

        statistics = (
            db.session.query(Domains, Statistics)
            .join(
                Statistics,
                Statistics.stats_domain_id == Domains.domain_id,
                isouter=True,
            )
            .offset((page_number - 1) * max_per_page)
            .limit(max_per_page)
            .with_entities(
                Domains.domain_name,
                Domains.domain_type,
                Statistics.stats_client_ip,
                Statistics.stats_request_count,
            )
        )
        # statistics = db.session.query(Statistics, Domains)\
        #              .join(Domains, Domains.domain_id == Statistics.stats_domain_id, isouter=True)\
        #              .offset((page_number-1)*max_per_page).limit(max_per_page)\
        #              .with_entities(Domains.domain_name, Domains.domain_type, Statistics.stats_client_ip, Statistics.stats_request_count)

        # statistics = db.session.query(Statistics).offset((page_number-1)*max_per_page).limit(max_per_page).all()
        return num_statistics, statistics


def main():

    # db_delete()
    Statistics.db_init()

    test1 = Statistics(1, "10.0.0.1")
    test2 = Statistics(1, "10.0.0.2")
    test2 = Statistics(2, "10.0.0.2")

    Statistics.db_statistics_add(test1)
    Statistics.db_statistics_add(test2)
    Statistics.db_statistics_add(test2)

    db.session.close()


if __name__ == "__main__":
    main()
