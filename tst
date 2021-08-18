release: python manage.py migrate

web: gunicorn followup.wsgi --log-file -