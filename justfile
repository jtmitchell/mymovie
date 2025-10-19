# This file will load a .env file to allow overriding values.

set dotenv-load := true

VERSION := shell("uv version --short")

# This list of available targets
default:
    @just --list

# Install python DEV dependancies
install:
    uv sync
    uv run pre-commit install --hook-type pre-commit

# uv run a command
run +options:
    uv run {{options}}

# Run the tests
test +options="":
    uv run pytest src/ {{options}}

# Build the docker image
build target="production":
    docker build -f Dockerfile \
    --target production \
    --label "org.opencontainers.image.revision"="v{{VERSION}}" \
    .

version:
    @echo {{VERSION}}

# Run the uv version command
bumpversion +options="":
    uv version {{options}}

# Start new develpment cycle with new patch and release candidate
bump_patch +options="":
    uv version --bump rc {{options}} --commit
    git push

# Bump the version for a release. Make tag and commit
bump_release +options="":
    uv version --bump stable {{options}} --tag --commit
    git push && git push --tags
