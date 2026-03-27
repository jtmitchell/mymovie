# This file will load a .env file to allow overriding values.

set dotenv-load := true
set shell := ["bash", "-c"]
set working-directory := 'src/'

# This list of available targets
default:
    @just --list

# Install python DEV dependancies
install:
    pdm install --frozen-lockfile --plugins
    pdm run pre-commit install --hook-type pre-commit

# pdm run a command
run +options:
    pdm run {{ options }}

# Run the tests
test +options="":
    pdm run pytest {{ options }}

# Build the docker image
build target="production":
    docker build -f Dockerfile \
    --target production \
    --label "org.opencontainers.image.revision"="v$(pdm version)" \
    .

version:
    @pdm version

# Run the pdm bump version command
bumpversion +options="":
    pdm bump {{ options }}

# Start new development cycle with new patch and release candidate
bump_patch +options="":
    pdm bump pre-release --pre alpha {{ options }}
    git add pyproject.toml && git commit -m "Bump version to $(pdm version)"
    git push

# Bump the version for a release. Make tag and commit
bump_release +options="":
    pdm bump release {{ options }}
    git add pyproject.toml && git commit -m "Release v$(pdm version)"
    git tag "v$(pdm version)"
    git push && git push --tags
