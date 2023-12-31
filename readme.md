# SOLID FastAPI Skeleton API

Presenting production ready SOLID API architecture with python/FastAPI. 
This skeleton project brings together in an oppinionated way OOP patterns
in order to build a production ready web API.

# Concepts

- Following closely on Clean Architecture concepts as described in [the book by Robert C. Martin](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [SOLID principles](https://en.wikipedia.org/wiki/SOLID) are central
- Layered architecture using vendor-agnostic pluggable services (data layer, message queue, etc)
- CI/CD with githubactions

A web API built with this blueprint has these parts:
1. **Core library** - all interfaces and services that implement those so that application components can easily share
2. **Application components** - actual implementation of the business logic. Each components extends its own repository
as it can have special methods/queries
3. **Web API Container** - ties up together the app by instantiating project wide dependencies and handling http requests
and calling the application component logic

# Benchmarks (async fastapi vs syncfastapi)
There are 2 reports made using Locust by running in production mode the async version and the sync version of this.
Read both the reports at _BENCHMARK/reports. Both projects were dockerized, served using Gunicorn and Nginx.
Configuration for nginx was the same for both, but gunicorn used different setups:
1. async app: 1 uvicorn worker (best results)
2. sync app: 4 uvicorn workers (best results)
Note that running FastApi with gunicorn can **only** be using the uvicorn worker type.

   

# CORE

This is the core shared library. It contains all the commonly used services, repositories and interfaces.
It's used inside the model components and the container app as a python package.

It's the top most depencency component:
![dependencies and interfaces diagram](https://raw.githubusercontent.com/smileservices/async-solid-web-api/master/components.png)

<hr>

**core.services**
- Contains Abstract interfaces and adapters to services like google secrets, rabbitmq, etc

**core.interfaces**
- Contains services like Secrets, Message Queue, that implement the abstract interfaces

**core.repository**
- Contains data layer interfaces and adapters
- Uses [data-persistance-repository](https://github.com/smileservices/data_persistence_repository) library
- If you want to use noSql databases, make your own repository that implements the repository interface

# Application Components

- interface.py - the entrypoint in interacting with the business logic
- dependencies.py - declares the required services and allows to easily set it up
- models.py - business data structures
- tables.py - data layer structures
- serializers.py - input/output data structures
- tests

Interface exposes all ways that it's possible to interract with the component. It is the responsability of the higher
layer (the container) to inject the required dependency.

# Web API Container
- dependencies.py - declares the API dependencies
- bootstrap.py - instantiates the API dependencies, config service
- main.py - entrypoint of the web application
- Can be FastAPI, Flask, whatever
- use an async supporting web server for working async


## Alembic Migrations

1. Create migrations: `alembic revision --autogenerate -m "<title>"`
2. Inspect newly created migration in `/alembic/versions`
3. Apply migration `alembic upgrade head`

## Testing

For tests we use `pytest` and they are run using docker-compose

- execute `make test` :: runs the test suite inside the docker context


## Enviroment Variables
We use `.env` file that sits inside the application folder `/api`. Can use any type of secret service, just create a new SecretService in Core.


## Development & User Guide

Most of the development and the domain logic are modelled into the `model components` so don't
stuff a lot of things into the FastAPI handlers.

**There are 2 ways of setting up the development enviroment:**

**1. Create a virtual python enviroment** and use that to develop and run tests

- easy and fast to setup
- suited for doing rapid development
- make sure to set up the env vars

**2. Set your python interpreter to run through docker**

- run `make test` will create the docker image for running the app under docker-compose
- set your python interpreter to `_DOCKER/docker-compose.yml` file for the service `fast-api-skeleton`
- can use breakpoints in PyCharm

# Production Deployment

**run using gunicorn**
For production deployment, start the application using gunicorn uvicorn workers. 
Set the number of workers in relation to available cores (1 worker per core). The best practice is to manage
gunicorn process using `supervisord`. Don't forget to set up logging paths.

**nginx as reverse proxy**
Use nginx as a reverse proxy to direct traffic onto gunicorn. Don't forget to set up logging paths.