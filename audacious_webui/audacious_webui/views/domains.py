# -*- encoding: utf-8 -*-
import logging
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app
from audacious_webui.models.domains import Domains
from audacious_webui.forms import DomainsForm
from werkzeug.exceptions import abort
from math import ceil

LOGGER = logging.getLogger(__name__)
domains = Blueprint("domains", __name__)
MAX_PER_PAGE = 10


# App main route + generic routing
@domains.route("/domains", methods=["GET"])
@domains.route("/domains/page/<int:page>", methods=["GET"])
def page_domains(page=1, max_per_page=MAX_PER_PAGE):
    try:
        num_domains, domains = Domains.db_domains_get_paginate(current_app.session, page, max_per_page)
        page_number = ceil(num_domains / max_per_page)

        LOGGER.info(num_domains)

        form_domain = DomainsForm(request.form)
        LOGGER.info(f"domain name = {form_domain.domain_name.data}")
        LOGGER.info(f"domain type = {form_domain.domain_type.data}")
        LOGGER.info(f"domain active = {form_domain.domain_isactive.data}")

        return render_template(
            "layouts/default.html",
            content=render_template(
                "pages/domains.html",
                domains=domains,
                page=page,
                page_name="domains.page_domains",
                page_number=page_number,
                form=form_domain,
            ),
        )
    except Exception as e:
        LOGGER.error(e)
        abort(404)


@domains.route("/domains/insert", methods=["GET", "POST"])
def page_domains_insert():
    try:
        form = DomainsForm(request.form)
        LOGGER.info(f"domain name = {form.domain_name.data}")
        LOGGER.info(f"domain type = {form.domain_type.data}")
        LOGGER.info(f"domain active = {form.domain_isactive.data}")

        if form.validate_on_submit():
            domain_name = form.domain_name.data
            domain_type = form.domain_type.data
            domain_isactive = form.domain_isactive.data

            if domain_name and domain_type and domain_isactive:
                LOGGER.info(
                    f"Trying to add a new domain --> {domain_name}/{domain_type}/{domain_isactive}"
                )
                new_domain = Domains(domain_name, domain_type, domain_isactive)
                new_domain.db_domains_add(current_app.session)
        else:
            flash("incomplete form")

    except Exception as e:
        LOGGER.error(str(e))
        flash(str(e))
        # abort(404)
        pass
    finally:
        return redirect(url_for("domains.page_domains"))


@domains.route("/domains/update", methods=["GET", "POST"])
def page_domains_update():
    try:
        form = DomainsForm(request.form)
        LOGGER.info(f"domain name = {form.domain_name.data}")
        LOGGER.info(f"domain type = {form.domain_type.data}")
        LOGGER.info(f"domain active = {form.domain_isactive.data}")

        if form.validate_on_submit():
            domain_id = request.form["domain_id"]
            domain_name = form.domain_name.data
            domain_type = form.domain_type.data
            domain_isactive = form.domain_isactive.data

            LOGGER.info(
                f"Trying to edit {domain_id} --> {domain_name} - {domain_type} - {domain_isactive}"
            )
            Domains.db_domains_update(
                current_app.session,
                domain_id,
                {
                    "domain_name": domain_name,
                    "domain_type": domain_type,
                    "domain_isactive": domain_isactive,
                },
            )

        else:
            flash("incomplete form")

    except Exception as e:
        LOGGER.error(str(e))
        flash(str(e))
    finally:
        return redirect(url_for("domains.page_domains"))


@domains.route("/domains/delete", methods=["GET", "POST"])
def page_domains_delete():
    try:
        if request.method == "POST":
            domain_id = request.form["domain_id"]
            LOGGER.error(f"DELETE --> domain id {domain_id}")
            Domains.db_domains_delete_by_id(current_app.session, domain_id)

            return redirect(url_for("domains.page_domains"))
        else:
            return "ok"
    except Exception as e:
        LOGGER.error(e)
        abort(404)
