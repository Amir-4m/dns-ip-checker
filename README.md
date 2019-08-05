# Domain DNS Controller 

## local_settings.py
Project local settings

```python
DEBUG = True
DEVEL = True

ALLOWED_HOSTS = []

DB_ENGINE = 'django.db.backends.mysql'
DB_HOST = ''
DB_PORT = ''
DB_NAME = ''
DB_USER = ''
DB_PASS = ''

CACHE_BACKEND = 'django.core.cache.backends.memcached.MemcachedCache'
CACHE_HOST = 'localhost:11211'

CELERY_BROKER_USER = 'guest'
CELERY_BROKER_PASS = 'guest'
CELERY_BROKER_HOST = 'localhost:5672/'

STATIC_URL = '/static/'

CLOUDFLARE_EMAIL = 'YOUR EMAIL'
CLOUDFLARE_API_KEY = 'YOUR API KEY'

NETCAT_TIMEOUT = 1

# Promoter
TELEGRAM_API_ID = 0
TELEGRAM_API_HASH = ''
PROXY_HOST = ''
PROXY_PORT = 0

# Notifier
BOT_TOKEN = ''
```