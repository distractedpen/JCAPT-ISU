JCAPT-ISU

This project is my cs695 (Computer Research) project.

The Japanese Teacher and I are looking into designing an Adaptive Learning System for learning Japanese in the classroom. In this research, a CAPT (Computer Assisted Pronunciation Teacher) system was deamed useful. This repo is my work in designing and implementing ideas for a CAPT system for learning Japanese pronunciation.

#Directory Structure

The `client` directory is the frontend. When the service is running (see `service`), the user can record their voice and get feed back on their pronunciation. Currently limited to the select few sentences/dialogues set by the service.

The `scripts` directory currently contains the startup script for the service, `start_service.sh`. This currently only works on linux, looking to expand to WSL.

The `service` directory contains the following subdirectories:
    `audio` - currently a drop point for audio files recieved from `client` and a place for the service to convert the `.ogg` files to `.wav` files. Currently files are deleted after they are used by vosk for speech to text. Currently looking at how these audio files should be stored.

    `logs` - currently a drop point for the log text outputted by `ffmpeg`. Will also be the place for `vosk` to output its log information.

    `src` - source code for the service.

    `text` - currenty a drop point for the text files used by the service.


#How to Use:

    - System currently only works on Linux.
    - Requires pipenv.
    - Download this repo using git, from the root directory run `./scripts/run_install.sh` to install the pipenv virtual environment.
    - Download a model from https://alphacephei.com/vosk/models. Extract the archive and rename the directory to `model`. Place new `model` directory in the `service` directory.
    - Create a list of text for the service to read. (Format WIP). Place file in `text` directory.
    - Run ./scripts/start_service.sh to start the flask backend.
    - Open the file `client/index.html` in a web browser.