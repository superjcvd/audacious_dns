# -*- encoding: utf-8 -*-
import logging
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from audacious_webui.models.statistics import Statistics
from werkzeug.exceptions import abort
from math import ceil

LOGGER = logging.getLogger(__name__)
statistics = Blueprint("statistics", __name__)
MAX_PER_PAGE = 10


# App main route + generic routing
@statistics.route("/statistics", methods=["GET"])
@statistics.route("/statistics/page/<int:page>", methods=["GET"])
def page_statistics(page=1, max_per_page=MAX_PER_PAGE):
    try:
        if 0 <= page <= 100:
            statistics_number, statistics = Statistics.db_statistics_get_paginate(
                current_app.session, page, max_per_page
            )
            page_number = ceil(statistics_number / max_per_page)

            return render_template(
                "layouts/default.html",
                content=render_template(
                    "pages/statistics.html",
                    statistics=statistics,
                    page=page,
                    page_name="statistics.page_statistics",
                    page_number=page_number,
                ),
            )
        else:
            LOGGER.error("KO")
            return "ko"
    except Exception as e:
        LOGGER.error(e)
        abort(404)
