#!/bin/sh

# Run this script ON THE SERVER, not locally.

docker-compose -f docker-compose.yml -f docker-compose.staging.yml build

mkdir -p certificates

if [ "$(ls -A certificates)" ]; then
    :
else
    # Run letsencrypt initialization
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml stop && \
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml run --service-ports nginx /init_letsencrypt.sh
fi

docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
