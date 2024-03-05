@echo off

python manage.py migrate
python manage.py test
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000
