# pull official base image
FROM python:3.8-slim-buster


# install Pipenv and other app dependencies:
RUN apt-get update && apt-get install python3-dev libffi-dev gcc curl musl-dev netcat-openbsd -y
RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.8
RUN pip3 install pipenv

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# add and install requirements
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system --dev

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app
