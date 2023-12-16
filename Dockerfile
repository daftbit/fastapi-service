# Base container
FROM python:3.11-slim-bullseye as release-base

WORKDIR /app

RUN apt-get update \
    && apt-get install -y jq curl gcc bash libffi-dev openssl libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip and poetry dependencies
RUN pip install poetry
ENV PATH="/root/.local/bin:${PATH}"
COPY poetry.lock /app/
COPY pyproject.toml /app/
RUN poetry config installer.max-workers 10
RUN poetry install --no-dev

# Test container
FROM release-base as test
RUN poetry install
COPY src /app/src

# Release container
FROM release-base as release
COPY docker-entrypoint.sh /
COPY alembic /app/alembic
COPY src /app/src

# Environment variables
ARG VERSION="1.0.0"
ENV VERSION="$VERSION"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENTRYPOINT [ "/docker-entrypoint.sh" ]
#CMD poetry run gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 src.main:app --log-config logging.conf --workers=3
CMD poetry run gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 src.main:app --workers=3




