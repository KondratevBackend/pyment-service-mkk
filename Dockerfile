ARG VIRTUAL_ENV_PATH=/opt/venv

FROM python:3.13-bullseye as builder
WORKDIR /app
ARG VIRTUAL_ENV_PATH

ENV VIRTUAL_ENV=${VIRTUAL_ENV_PATH:-/opt/venv} \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=2.2.1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends build-essential \
  && python -m venv ${VIRTUAL_ENV} \
  && pip install --no-cache-dir --upgrade pip --upgrade setuptools \
  && pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
  && poetry self add poetry-plugin-export

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o ./requirements.txt \
  && pip install --no-cache-dir -r requirements.txt

FROM python:3.13-bullseye as app
WORKDIR /app

ARG VIRTUAL_ENV_PATH
ENV VIRTUAL_ENV=${VIRTUAL_ENV_PATH:-/opt/venv} \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN apt-get update --fix-missing \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY . .
