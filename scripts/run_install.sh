#!/bin/bash

PYTHON=$(python3 -V | awk '{ print $2 }' | awk -F. '{ print $1"."$2 }')

if [ PYTHON != "3.9" ];
then
    echo "Python3.9 required for service"
    exit
fi

pushd service
pipenv install
popd
