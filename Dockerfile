FROM docker.io/library/python:3.10

LABEL Version="1.0.0-rc-0"
LABEL Description="Application for tracking movies."

# Create 'app' user with id=1000
RUN groupadd --force --gid 1000 app
RUN useradd --uid 1000 --gid 1000 --no-create-home app

ENV VIRTUAL_ENV=/var/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /var/app

COPY requirements requirements/
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache -r requirements.txt

COPY manage.py /var/app
COPY bin /var/app
COPY app /var/app
COPY movies /var/app
COPY users /var/app
COPY utils /var/app

# Collect the static files
RUN python manage.py collectstatic --noinput --no-color

USER app
EXPOSE 80 9000
ENTRYPOINT ["/var/app/bin/start-app"]
