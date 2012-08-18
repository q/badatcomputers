from settings import *

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_HOST_USER = 'badatcomputers@gmail.com'
EMAIL_HOST_PASSWORD = '{EMAIL_PASSWORD}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gungnir',                      # Or path to database file if using sqlite3.
        'USER': 'badatcomputers',                      # Not used with sqlite3.
        'PASSWORD': '{DB_PASSWORD}',                  # Not used with sqlite3.
        'HOST': 'djangodash-db.cqxkmfigpnvp.us-east-1.rds.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

