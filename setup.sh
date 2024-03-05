#!/bin/bash

# Run Django management commands
python manage.py migrate
python manage.py test

# Create Django superuser
python manage.py createsuperuser --noinput

# Run Django development server
python manage.py runserver 0.0.0.0:8000