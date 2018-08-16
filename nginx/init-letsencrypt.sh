#!/bin/sh
certbot -n certonly --standalone --force-renewal --preferred-challenges http -d xproj-api.hyunwoo.me --agree-tos --email khw0726@kaist.ac.kr
