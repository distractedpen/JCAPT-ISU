#!/bin/bash


pushd service/src
pipenv run python3 app.py
popd

for file in service/audio/recordings
do
    if [ -f "$file" ]
    then
        rm -rf $file
    fi
done

