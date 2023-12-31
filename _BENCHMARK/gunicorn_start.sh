#!/bin/bash
NAME=async-web-api
DIR=/project
USER=root
GROUP=root
WORKERS=1
BIND=0.0.0.0:8000
LOG_LEVEL=debug

exec gunicorn \
        api.main:app \
        --name ${NAME} \
        --workers ${WORKERS} \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind ${BIND} \
        --user=root \
        --group=${GROUP} \
        --log-level=${LOG_LEVEL} \
        --log-file=- \
        --chdir=/project
