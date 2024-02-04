ARG PYTHON_VERSION=3.11
FROM python:$PYTHON_VERSION

ENV PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    POETRY_CACHE_DIR="/vol/cache/poetry"

RUN apt-get update \
    && pip3 install poetry

RUN mkdir -p /vol/cache/poetry && \
    mkdir -p /vol/package/redbeanpython && \
    mkdir -p /vol/package/tests && \
    mkdir -p /vol/package/.coverage-reports

WORKDIR /vol/package

COPY /tests/pyproject.toml /vol/package/pyproject.toml

RUN groupadd -r package && \
    useradd -r -g package package && \
    chown -R package:package /vol/package && \
    chown -R package:package /vol/cache/poetry

RUN poetry install --no-interaction --no-ansi --no-root --no-directory

COPY /redbeanpython /vol/package/redbeanpython
COPY /tests /vol/package/tests

RUN poetry install --no-root --no-interaction --no-ansi
