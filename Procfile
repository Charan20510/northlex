web: gunicorn northlex.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A northlex worker --loglevel=info
