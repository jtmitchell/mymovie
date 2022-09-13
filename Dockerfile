ARG baseimage=ubuntu:22.04

FROM ${baseimage} as build

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-venv python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv --copies /var/.venv
ENV PATH="/var/.venv/bin:$PATH"

WORKDIR /var/app
COPY requirements requirements/
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache -r requirements.txt

COPY manage.py .
COPY bin bin/
COPY app app/
COPY movies movies/
COPY users users/
COPY utils utils/

RUN chmod +x /var/app/bin/start-app

# Collect the static files
ARG DJANGO_SETTINGS_MODULE=app.settings.dockerbuild
RUN python3 manage.py collectstatic --noinput --no-color

# Stage for the tests
FROM build as test

WORKDIR /var/app
RUN python3 -m pip install --no-cache -r requirements/test.txt
COPY ["mypy.ini", "pytest.ini", "/var/app/"]
ARG DJANGO_SETTINGS_MODULE=app.settings.test
RUN mypy /var/app/
RUN pytest /var/app/

# Final stage.
FROM ${baseimage} as prod

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt install -y --no-install-recommends \
    python3 python3-pip \
    tzdata \
    netcat-openbsd \
    libpq5 postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ENV TZ="Pacific/Auckland"
ENV PATH="/var/.venv/bin:$PATH"
COPY --from=build /var/.venv /var/.venv
COPY --from=build /var/app /var/app

# Create 'app' user with id=1000
RUN groupadd --force --gid 1000 app
RUN useradd --uid 1000 --gid 1000 --no-create-home app

LABEL Version="1.0.0-rc-1"
LABEL Description="Application for tracking movies."

WORKDIR /var/app
USER app
VOLUME ["/var/tmp"]
EXPOSE 8000 9000
ENV SERVER_PORT=8000

ENTRYPOINT ["/var/app/bin/start-app"]
