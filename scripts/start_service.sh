#!/bin/bash

export FLASK_APP=app.py
pushd service/src
pipenv run flask run --host 0.0.0.0 --port 8001 --cert ~/ssl_certs/server.crt --key ~/ssl_certs/server.key
popd

