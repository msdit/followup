# syntax=docker/dockerfile:1
FROM python:3.8-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps
WORKDIR /app
COPY ./app/requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./app/ /app/

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn followup.wsgi:application --bind 0.0.0.0:$PORT