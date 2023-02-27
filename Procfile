release: sh -c 'python manage.py migrate'
web: python manage.py migrate && gunicorn social_media.wsgi