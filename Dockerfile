FROM  python:3.9.16-alpine3.17

ENV PYTHONUNBUFFERED = 1

WORKDIR /app

RUN apk update \
    && pip install --upgrade pip 

RUN apk add musl-dev mariadb-dev gcc

RUN pip install mysqlclient

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./  ./

CMD [ "python","manage.py","runserver","0.0.0.0:8080" ]