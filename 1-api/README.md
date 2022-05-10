# Californian Housing API

Welcome to this great FastAPI application that provides data on [California Housing Market](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html). There are two endpoints:

1. a `/data` that provides raw data 
2. a `/predictions` endpoint that predicts prices given a house informations

## To make it work 

You will need to provide AWS credentials that Jedha can give you to make this code full functional.

## Deploy FastAPI to Docker 

There is a bit of a conflict here, which is that Heroku uses WSGI web server framework whereas FastAPI uses ASGI. To work around that problem, you need to have in your Dockerfile a command that looks like this:

`gunicorn api:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker`

More info here: https://stackoverflow.com/questions/63424042/call-missing-1-required-positional-argument-send-fastapi-on-app-engine/70404102#70404102

