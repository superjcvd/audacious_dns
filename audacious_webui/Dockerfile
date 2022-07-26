# syntax=docker/dockerfile:1
ARG application=audacious_webui

### docker build --no-cache --tag audacious_webui .
### docker build --tag audacious_webui .

FROM python:slim-bullseye
WORKDIR /build
COPY . .
RUN pip3 install -r requirements.txt
RUN python3 -m black --check .
# RUN python3 -m pytest
RUN python3 -m build


FROM python:slim-bullseye
USER root
WORKDIR /${application}

RUN apt-get update \
    && apt-get -y dist-upgrade
RUN apt-get autoremove \
    && apt-get clean

COPY --from=0 /build/dist/${application}*.tar.gz ./${application}.tar.gz
RUN pip3 install ${application}.tar.gz

# COPY alembic.ini .
# COPY migrations migrations
RUN mkdir -p /var/audacious_dns/database/
COPY audacious_webui/database/database.db /var/audacious_dns/database/database.db

EXPOSE 8080/tcp

# ENV FLASK_ENV=development
CMD [ "waitress-serve", "--trusted-proxy=*", "--trusted-proxy-headers=x-forwarded-proto", "--call", "audacious_webui:create_app" ]
