
import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '{{ remote_dir }}/data/db.sqlite',
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        #'BINARY': True,
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = 'artexer'

MEDIA_ROOT = os.path.join('{{remote_dir}}', 'media', 'media')
STATIC_ROOT = os.path.join('{{remote_dir}}', 'media', 'static')

SENTRY_DSN = 'https://bc2d54d113414511bb231958ca0002b7:7809ecbdb0ec46c589ac92d0b6272792@app.getsentry.com/283'

{{settings_logging}}
