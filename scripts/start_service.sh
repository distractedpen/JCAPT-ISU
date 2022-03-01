#!/bin/bash


pushd service/src
pipenv run flask run
popd
