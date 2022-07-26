# syntax=docker/dockerfile:1
ARG application=audacious_core

FROM debian:bullseye-slim
USER root
WORKDIR /${application}

RUN apt-get update \
    && apt-get -y dist-upgrade\
    && apt-get clean

RUN apt-get -y install nano \
    && apt-get -y install sudo \
    && apt-get -y install apt-utils \
    && apt-get -y install pdns-recursor \
    && apt-get -y install dnsdist \
    && apt-get -y install sqlite3 \
    && apt-get -y install lua-sql-sqlite3 \
    && apt-get -y install procps \
    && apt-get -y install supervisor

RUN apt-get autoremove \
    && apt-get clean

COPY system/ /
# COPY resources/database_dev.db /var/audacious_dns/database/database.db
# RUN groupadd database
# RUN usermod -aG database pdns
# RUN chgrp -R database /var/audacious_dns/database/
# RUN chmod -R 664 /var/audacious_dns/database/
RUN mkdir -p /var/audacious_dns/database/
RUN chown -R pdns:pdns /var/audacious_dns/database/

# RUN pip3 install ${application}.tar.gz
RUN mkdir -p /var/run/pdns-recursor
RUN chown pdns:pdns /etc/dnsdist/dnsdist.conf

EXPOSE 53/udp
EXPOSE 853/tcp
EXPOSE 5300/tcp

CMD ["/usr/bin/supervisord"]

### docker build --no-cache --tag dns .