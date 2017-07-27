<p align="center">
  <img src="/web/static/logo.png" width="100"/>
</p>

<h1 align="center">xproj-backend</h1>

A Django application that serves as the API for our client app.
Data storage, authentication, geocoding, news aggregator, and recommendation system.

## Setup

- You need [Docker](https://www.docker.com/get-docker) to run locally. It's very easy to set up on all platforms.
- `docker-compose up -d` for setting up the containers. This will take a few minutes.
- `docker-compose run web python3 manage.py migrate` for database setup
- Download the shapefiles from [here](http://snugis.tistory.com/127), extract and put into a folder `data/voting-districts/`
- `docker-compose run web python3 manage.py load_spatial_data` to import spatial data
- Unzip the file `data/promises.zip` into a folder `promises`
- `docker-compose run web python3 manage.py load_promise_data` to import promise data

## How to run

    docker-compose up -d

Go to [http://localhost:8000/](http://localhost:8000/)

## API usage

[Details about authentication endpoints](http://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html)

    # Signup
    POST http://localhost:8000/api/auth/signup/ email=... password1=... password2=...
    
    # Login
    POST http://localhost:8000/api/auth/login/ email=abc@abc.com password=xxx

    # Request url that needs authentication
    GET url "Authorization:Token <insert key obtained from signup or login>"
