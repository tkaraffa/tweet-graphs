# Top level build args
ARG build_for=linux/amd64

##
# base image (abstract)
##
FROM --platform=$build_for python:3.10.7-slim-bullseye as base

ARG BASE_REQUIREMENTS_SRC_PATH
ARG WHEEL_REQUIREMENTS_SRC_PATH
ARG DIST_PATH
ARG dbt_bigquery_ref=dbt-bigquery@v1.4.0b1

RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y --no-install-recommends \
  git \
  ssh-client \
  software-properties-common \
  make \
  build-essential \
  ca-certificates \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo BASE_REQUIREMENTS_SRC_PATH=$BASE_REQUIREMENTS_SRC_PATH
RUN echo WHEEL_REQUIREMENTS_SRC_PATH=$WHEEL_REQUIREMENTS_SRC_PATH
RUN echo DIST_PATH=$DIST_PATH

RUN pip install --upgrade pip setuptools

ARG SERVICE
COPY $SERVICE/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY $DIST_PATH ./dist

ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8


WORKDIR /usr/app/
COPY . .
RUN dbt deps

ENV DBT_PROFILES_DIR=/usr/app
ENTRYPOINT ["dbt"]
