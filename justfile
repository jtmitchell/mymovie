VERSION := "1.0.0-rc-0"

set dotenv-load := true

# This list of available targets
default:
    @just --list

# Run the tests
test:
    pytest

# Install the python packages (prod and dev)
install:
    @just install_prod
    @just install_dev
# Install the PROD python packages
install_prod:
    python3 -m pip install --upgrade pip
    python3 -m pip install -r ./requirements/production.txt
# Install the DEV python packages
install_dev:
    python3 -m pip install -r ./requirements/develop.txt
    pre-commit install --hook-type pre-commit --hook-type commit-msg

# Uninstall the python packages
uninstall_pip:
    #!/usr/bin/env bash
    pip uninstall -y -r <(pip freeze)


# Run the bump2version command, build will increment the release candidate
bumpversion +options="build":
    bump2version {{options}}

# Start new develpment cycle with new patch and release candidate
patch_version +options="":
    bump2version patch {{options}} --commit
    git push

# Bump the version for a release. Make tag and commit
release_version:
    bump2version release --tag --commit
    git push && git push --tags
