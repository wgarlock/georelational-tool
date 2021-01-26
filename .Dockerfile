# Future addition
FROM python:3.7-ubuntu:bionic

ADD /requirements.txt app/requirements.txt
ADD /region_builder app/region_builder
ADD /project app/project
ADD /manage.py app/manage.py

RUN set -ex \
    && apk add --no-cache --virtual .build-deps git libffi-dev libxml2-dev\
    libxslt-dev postgresql-dev jpeg-dev build-base memcached binutils libproj-dev gdal-bin \
    && wget https://download.osgeo.org/geos/geos-3.9.0.tar.bz2 \
    && tar xjf geos-3.9.0.tar.bz2 \
    && cd geos-3.9.0 \
    && ./configure \
    && make \
    && sudo make install \
    && cd .. \
    
    && wget https://download.osgeo.org/proj/proj-7.2.1.tar.gz\
    && wget https://download.osgeo.org/proj/proj-datumgrid-1.8.tar.gz\
    && tar xzf proj-7.2.1.tar.gz\
    && cd proj-7.2.1/nad\
    && tar xzf ../../proj-datumgrid-1.8.tar.gz\
    && cd ..\
    && ./configure\
    && make\
    && sudo make install\
    && cd ..\
    && wget https://download.osgeo.org/gdal/3.2.1/\
    && tar xzf gdal-3.2.1/.tar.gz \
    && cd gdal-3.2.1\
    && ./configure \
    && make \
    && sudo make install \
    && cd .. \
    && createdb region_builder\
    && psql region_builder\
    > CREATE EXTENSION postgis;\
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps \
    && cd app \
    && touch .env \
    && ls -all \
    && cd wheels \
    && ls -all

WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "project.wsgi:application"]