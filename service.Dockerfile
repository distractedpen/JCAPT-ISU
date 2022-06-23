FROM python

RUN apt-get update && apt-get install ffmpeg -y

COPY ssl/ /home/app/ssl/

WORKDIR /home/app/service

COPY ./service ./

RUN pip install pipenv
RUN pipenv install

WORKDIR /home/app/service/src

CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0", "--port", "40089", "--cert", "/home/app/ssl/server.crt", "--key", "/home/app/ssl/server.key"]
# > ../logs/log.txt 2> ../logs/log.txt"