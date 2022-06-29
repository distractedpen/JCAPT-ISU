FROM python

RUN apt-get update && apt-get install ffmpeg unzip tree -y

COPY ssl/ /home/app/ssl/

WORKDIR /home/app/service

# Get Model
RUN wget https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip
RUN unzip vosk-model-small-ja-0.22.zip
RUN mv vosk-model-small-ja-0.22 model
RUN rm vosk-model-small-ja-0.22.zip

COPY ./service ./

RUN pip install pipenv
RUN pipenv install

CMD pipenv run flask run --host $FLASK_SERVICE_HOST --port $FLASK_SERVICE_PORT --cert $SSL_DIR/server.crt --key $SSL_DIR/server.key