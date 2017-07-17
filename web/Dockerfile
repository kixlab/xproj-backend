# Linux Alpine + Python3 + PostgreSQL + PostGIS 

FROM frolvlad/alpine-python3

RUN adduser -D -g '' app

# Install binary dependencies
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
  # replacing default repositories with edge ones
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
  # Add the packages, with a CDN-breakage fallback if needed
  && apk add --no-cache --update $PACKAGES || \
    (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES)

# Setup app dir
RUN mkdir -p /usr/src/app

# Install pip packages
WORKDIR /usr/src/app/
ADD requirements.txt /usr/src/app/requirements.txt
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Copy rest of source code. Doing this in the end improves Docker caching
COPY . /usr/src/app

RUN chmod -R 777 /usr/src/app
