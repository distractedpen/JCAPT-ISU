#!/bin/bash

export FLASK_APP=app.py
pushd service/src
pipenv run flask run --host cs.indstate.edu --port 40089 --cert ~/ssl_certs/server.crt --key ~/ssl_certs/server.key
popd

