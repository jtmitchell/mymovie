# syntax=docker.io/docker/dockerfile:1.7-labs
# Allows use of --exclude in the COPY

# ---
# Base linux layer
# ---
FROM ubuntu:24.04 AS linux-base

# Assure UTF-8 encoding is used.
ENV LC_CTYPE=C.utf8
# Location of the virtual environment
ENV UV_PROJECT_ENVIRONMENT="/venv"
# Location of the python installation via uv
ENV UV_PYTHON_INSTALL_DIR="/python"
# Byte compile the python files on installation
ENV UV_COMPILE_BYTECODE=1
# Python verision to use
ENV UV_PYTHON=python3.12
# Tweaking the PATH variable for easier use
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"
# Update debian
RUN apt-get update
RUN apt-get upgrade -y

# Install general required dependencies
RUN apt-get install --no-install-recommends -y tzdata

# ---
# Base Python install
# ---
FROM linux-base AS python-base
# Install debian dependencies
RUN apt-get install --no-install-recommends -y \
    build-essential \
    gettext

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create virtual environment and install dependencies
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ---
# Install the Python app
# ---
FROM python-base AS builder-base

ARG DJANGO_SETTINGS_MODULE=config.settings.development
ARG DB_USER=
ARG DB_PASSWORD=
ARG DATABASE_URL=
ARG DJANGO_SECRET_KEY=

WORKDIR /var/app
COPY src/ /var/app
COPY ./docker /var/docker

# Build static files
RUN uv run python manage.py collectstatic --no-input

# ---
# Development container image
# ---
FROM builder-base AS devcontainer

# Install the development packages
RUN uv sync --frozen --no-install-project

# Start the development server
WORKDIR /var/app
EXPOSE 8000
CMD ["bash", "/var/docker/dev-entrypoint.sh"]

# ---
# Production container image
# ---
FROM linux-base AS production

# Copy python, virtual env and static assets
COPY --from=builder-base $UV_PYTHON_INSTALL_DIR $UV_PYTHON_INSTALL_DIR
COPY --from=builder-base $UV_PROJECT_ENVIRONMENT $UV_PROJECT_ENVIRONMENT
COPY --from=builder-base --exclude=uv.lock --exclude=pyproject.toml /var/app /var/app

# Start the application server
WORKDIR /var/app
EXPOSE 8000
CMD ["bash", "/var/docker/entrypoint.sh"]
