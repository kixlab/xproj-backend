#!/bin/sh

# The target of this script should be the remote server.
# Either run it ON the server or select the machine using docker-machine.

if (AWS_PROFILE=kixlab docker-machine env xproject-backend) then
    eval $(AWS_PROFILE=kixlab docker-machine env xproject-backend)
else
    echo "Check that your AWS credentials are stored in ~/.aws/credentials under the key [kixlab]."
    echo "It should look like this:"
    echo "[kixlab]"
    echo "aws_access_key_id = Axxxx"
    echo "aws_secret_access_key = xxxx"
    exit
fi


docker-compose -f docker-compose.yml -f docker-compose.staging.yml build

mkdir -p certificates

if [ "$(ls -A certificates)" ]; then
    :
else
    # Run letsencrypt initialization
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml stop && \
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml run --service-ports nginx /init-letsencrypt.sh && \
    touch certificates/done.txt
fi

docker-compose -f docker-compose.yml -f docker-compose.staging.yml run web python3 manage.py migrate

docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
