#!/bin/bash
python manage.py migrate
gunicorn alx_travel_app.wsgi:application
