# -*- coding: utf-8 -*-
# :Project:   SoL -- Dockerization setup
# :Created:   mer 30 mar 2016 21:08:50 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018, 2020 Lele Gaifax
#

FROM python:3.8-slim

MAINTAINER Lele Gaifax <lele@metapensiero.it>

# Install DejaVu fonts, used by all printouts
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    apt-get autoremove -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
       fonts-dejavu \
       && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

COPY requirements/base.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt && \
    python3 -m metapensiero.extjs.desktop --no-cache && \
    rm -f /tmp/requirements.txt

COPY . /usr/src/sol
RUN pip install --no-cache -e /usr/src/sol

WORKDIR /srv
RUN mkdir /srv/data /srv/data/backups /srv/data/emblems /srv/data/portraits && \
    soladmin create-config --password admin --alembic-dir /usr/src/sol/alembic --data-dir /srv/data /srv/data/config.ini && \
    soladmin initialize-db /srv/data/config.ini && \
    soladmin restore /srv/data/config.ini

COPY docker/entrypoint.sh /srv/entrypoint.sh

EXPOSE 6996
VOLUME /srv/data

ENTRYPOINT ["./entrypoint.sh"]
CMD ["start"]
