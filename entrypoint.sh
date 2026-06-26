#!/bin/sh

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput


echo "Starting Gunicorn server..."
exec gunicorn numb.wsgi:application --bind 0.0.0.0:${PORT:-8080}