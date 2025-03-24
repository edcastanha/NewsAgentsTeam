#!/usr/bin/env bash
# exit on error
set -o errexit
export DJANGO_SETTINGS_MODULE=core_dj.settings

python manage.py collectstatic --no-input

# Em Desenvolvimento Make Migrations para atualizar Tables
#python manage.py makemigrations

python manage.py migrate

python setup.py