# syntax=docker.io/docker/dockerfile:1.7-labs
# Allows use of --exclude in the COPY

# ---
# Builder layer
# ---
ARG PYTHON_VERSION=3.14
ARG PYTHON_BASE=${PYTHON_VERSION}-slim

# build stage
FROM python:$PYTHON_BASE AS builder

ARG DJANGO_SETTINGS_MODULE=config.settings.production
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DATABASE_URL=""
ENV DJANGO_SECRET_KEY="build-secret"

# install PDM
RUN pip install -U pdm
# disable update check
ENV PDM_CHECK_UPDATE=false

WORKDIR /var/app

# Install dependencies only (without the project) for better layer caching
RUN --mount=type=cache,target=/root/.cache/pdm \
    --mount=type=bind,source=pdm.lock,target=pdm.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    python3 -m venv /venv && pdm use -f /venv && \
    pdm install --frozen-lockfile --production --no-self --no-editable

# Update PATH to include venv
ENV PATH="/var/app/.venv/bin:$PATH"

COPY ./src /var/app

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/pdm \
    --mount=type=bind,source=pdm.lock,target=pdm.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    pdm install --frozen-lockfile --production --no-editable
# Build static files
RUN /venv/bin/python manage.py collectstatic --no-input

# ---
# Production container image
# ---
FROM python:$PYTHON_BASE AS production

WORKDIR /var/app

# Copy python, virtual env and static assets
COPY --from=builder --exclude=pdm.lock --exclude=pyproject.toml /var/app /var/app
COPY --from=builder /venv /venv

# Update the PATH
ENV PATH="/venv/bin:$PATH"
# Start the application server
WORKDIR /var/app
EXPOSE 8000
ENTRYPOINT ["/venv/bin/python3"]
CMD ["serve.py"]
