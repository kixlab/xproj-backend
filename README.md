# xproj-backend

A Django application that serves as the API for our web app.
Data storage, authentication, geocoding, and recommendation system.

## Setup

- You need [Docker](https://www.docker.com/get-docker) to run locally. It's very easy to set up on all platforms.
- Download the shapefiles from [here](http://snugis.tistory.com/127), extract and put into a folder `data/voting-districts/`
- `docker-compose up -d` for setting up the containers
- `docker-compose run web python3 manage.py migrate` for database setup
- `docker-compose run web python3 manage.py load_data` to import spatial data

## How to run

    docker-compose up -d

    Go to http://localhost:8000/
