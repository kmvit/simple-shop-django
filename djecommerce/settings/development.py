from .base import *

DEBUG = True
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = ['127.0.0.1']
STRIPE_SECRET_KEY = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

