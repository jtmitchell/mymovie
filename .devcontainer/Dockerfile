# https://hub.docker.com/r/microsoft/devcontainers-base
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

ENV PYTHONDONTWRITEBYTECODE=True \
    PYTHONUNBUFFERED=True

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ack jq wget curl pipx\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
