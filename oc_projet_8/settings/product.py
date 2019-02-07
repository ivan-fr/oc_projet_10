from . import *

SECRET_KEY = '-~aO;| F;rE[??/w^zcumh(91'
DEBUG = False
ALLOWED_HOSTS = ['18.188.245.231']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        "NAME": "purbeurre",
        "USER": "ivan",
        "PASSWORD": "hWfY7Uv82k7L9f2Sr._.",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
