#!/bin/bash


pushd service/src
pipenv run python3 app.py
popd

