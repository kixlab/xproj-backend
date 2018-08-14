# Linux Alpine + Python3 + PostgreSQL + PostGIS + Numpy

FROM frolvlad/alpine-python3

RUN adduser -D -g '' app

# Install binary dependencies (MAIN alpine versions)
ENV PACKAGES_NUMPY="\
  gcc \
  gfortran \
  build-base \
  wget \
  freetype-dev \
  libpng-dev \
  openblas-dev \
  python3-dev \
  gettext-dev \
  curl \
  unzip \
"
RUN apk add --no-cache --update-cache $PACKAGES_NUMPY
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# For KONLPY
RUN apk add --no-cache --update-cache openjdk7

# Install binary dependencies (EDGE alpine versions)
ENV PACKAGES="\
  postgresql-client \
  postgresql-dev \
  py3-psycopg2 \
  gdal \
  gdal-dev \
  geos \
  proj4 \
"
RUN echo \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
  && apk add --no-cache --update $PACKAGES || \
    (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES)

# For Pillow
RUN apk add --no-cache --update-cache libjpeg-turbo-dev zlib-dev libpng-dev libxml2-dev libxslt-dev py-lxml

# Setup app dir
RUN mkdir -p /usr/src/app

# Install pip packages, split into multiple requirements files for better Docker caching
WORKDIR /usr/src/app/
ADD requirements/nlp.txt /usr/src/app/requirements/nlp.txt
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements/nlp.txt
ADD requirements/base.txt /usr/src/app/requirements/base.txt
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements/base.txt
ADD requirements/api.txt /usr/src/app/requirements/api.txt
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements/api.txt
ADD requirements/extras.txt /usr/src/app/requirements/extras.txt
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements/extras.txt
ADD requirements/extras2.txt /usr/src/app/requirements/extras2.txt
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements/extras2.txt

# Copy rest of source code. Doing this in the end improves Docker caching
COPY . /usr/src/app

RUN chmod -R 777 /usr/src/app
