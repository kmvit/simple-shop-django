from .base import *

DEBUG = False
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgres_psycopg2",
        "NAME": 'your db-name',
		"USER": 'your db-name',
		"PASSWORD": 'your db-name',
		"HOST": 'your db-name',
		"PORT": 'your db-name',
		)
    }
}

STRIPE_PUBLIC_KEY=''
STRIPE_SECRET_KEY=''