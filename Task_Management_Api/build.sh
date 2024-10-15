#!/usr/bin/env bash
# This script sets up the environment for the Task Management API project.
# It performs the following steps:
# 1. Sets the shell to exit immediately if any command exits with a non-zero status.
# 2. Installs the required Python packages listed in the requirements.txt file.
# 3. Collects static files for the Django project without user input.
# 4. Applies database migrations to ensure the database schema is up to date.

set -o errexit

pip install -r requirements.txt

python manage.py test

python manage.py collectstatic --no-input

python manage.py migrate
