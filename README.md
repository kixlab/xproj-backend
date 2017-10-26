<p align="center">
  <img src="/web/frontend/static/logo.png" width="100"/>
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

## Setup OAuth

Go to [/oauth/applications/](http://localhost:8000/oauth/applications/) and follow the steps to setup a client (e.g. webapp, chromeextension). For browser based web-apps, set client type to "public" and grant type to "Authorization code". For apps that can send username and password directly, use "Resource owner password-based". You can specify a client id, e.g. 'chromeextension'. Since our apps are public, we don't need the client secret.

## API usage

Some endpoints are currently public, for others you will need authentication.

The API also acts as an OAuth provider, so it should be easy to plug it into existing authentication libraries. Please send POST data as FORM DATA to all OAuth endpoints. The rest of the API can handle both JSON and form data.

    # Signup
    POST http://localhost:8000/api/auth/signup/ username=... email=... password1=... password2=...
    
    # Obtain oauth token
    POST http://localhost:8000/oauth/token/ client_id=... grant_type=password email="email" password="password"

    # Refresh oauth token
    POST http://localhost:8000/oauth/token/ grant_type=refresh_token client_id=... refresh_token=...

    # Request url that needs authentication
    GET http://localhost:8000/api/auth/user/ "Authorization:Bearer <insert oauth token>" 

For OAuth consumers (doing the OAuth dance), use these settings:

    Authorization url: http://localhost:8000/oauth/authorize/ response_type=code client_id=...
    Token url: http://localhost:8000/oauth/token/ code=... grant_type=authorization_code... client_id=...

## Other views

* [/accounts/signup/](http://localhost:8000/accounts/signup/) for a signup frontend view
