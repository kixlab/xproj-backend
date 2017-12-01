#!/bin/sh -e

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

docker-compose -f docker-compose.yml -f docker-compose.staging.yml run web ./initial-setup.sh