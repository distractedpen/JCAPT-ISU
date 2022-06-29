CAPT-ISU

This project is my cs695 (Computer Research) project.

The Japanese Teacher and I are looking into designing an Adaptive Learning System for learning Japanese in the classroom. In this research, a CAPT (Computer Assisted Pronunciation Teacher) system was deamed useful. This repo is my work in designing and implementing ideas for a CAPT system for learning foreign language pronunciation and fluency.

#Directory Structure

The `client` directory is the frontend. When the service is running (see `service`), the user can record their voice and get feed back on their pronunciation. Currently limited to the select few sentences/dialogues set by the service.

The `scripts` directory currently contains the startup script for the service, `start_service.sh`. This currently only works on Linux.

The `service` directory contains the following subdirectories:

    `logs` - a persistent directory to store the log text outputted by `ffmpeg`. Will also be the place for `vosk` to output its log information.

    `src` - source code for the service.

    `drills` - a persistent directory to store all drill sets and audio

    `users` - a persistent directory to store all user information

#How to Use:

    - Run containers by running `docker-compose up -d`
    - Client default runs on port 40088
    - Service default runs on port 40089
    - To change port numbers, edit the first number under 'ports' for each service in the docker-compose.yaml file.
    - Use docker-compose down to rm the containers