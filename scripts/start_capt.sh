#!/bin/bash

export FLASK_APP=app.py
pushd service/src
pipenv run flask run --host 0.0.0.0 --port 40089 --cert ~/ssl_certs/server.crt --key ~/ssl_certs/server.key > ../logs/log.txt 2> ../logs/log.txt &
popd
pushd client
npm start > log.txt 2> log.txt &
popd


