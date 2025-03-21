#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running setup.py..."
python setup.py

echo "Starting the application..."
# The user will likely need to add the command to start their application server (e.g., gunicorn) here.
# I will add a placeholder comment for this.
exec gunicorn --bind 0.0.0.0:5005 core.wsgi