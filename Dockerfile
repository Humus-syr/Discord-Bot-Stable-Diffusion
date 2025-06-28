# FROM us-central1-docker.pkg.dev/serverless-runtimes/google-22/runtimes/python313:latest as base
# FROM ubuntu:oracular
FROM python:3.12

USER root

RUN apt update \
  && apt upgrade -y \
  && apt install -y curl \
  && apt clean all \
  && apt autoremove

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY discord_src/ /app/discord_src/

WORKDIR /app/discord_src

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry install --no-dev

WORKDIR /app
COPY run_bot.py /app/run_bot.py

CMD ["python3", "run_bot.py"]

