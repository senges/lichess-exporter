# Mostly stolen to https://sourcery.ai/blog/python-docker/
FROM python:3.11-slim-buster as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY . /app
WORKDIR /app
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /app /app
WORKDIR /app

# Create and switch to a new user
RUN groupadd --gid 1000 lichess \
    && useradd --gid 1000 --uid 1000 --no-create-home lichess

USER lichess

# Run the application
ENTRYPOINT ["/app/.venv/bin/python"]
CMD ["/app/src/exporter.py"]
