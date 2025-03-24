"""Django settings for StockZero project - Production Grade."""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') # REQUIRED in .env or environment

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # Set to False in production

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') # Configure in .env
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'webapp.chessgame', 'webapp.frontend', 'management' # Added management app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stockzero.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'webapp' / 'frontend' / 'templates'], 'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug', 'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',
    ], },
}, ]

WSGI_APPLICATION = 'stockzero.wsgi.application'

# Database configuration - PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'stockzero_db'), # Configure in .env
        'USER': os.environ.get('DB_USER', 'stockzero_user'), # Configure in .env
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_db_password'), # Configure in .env - Strong password!
        'HOST': os.environ.get('DB_HOST', 'localhost'), # Configure in .env or use default
        'PORT': os.environ.get('DB_PORT', '5432'), # Configure in .env or use default
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # For production static file serving
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'webapp' / 'frontend' / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # Whitenoise for static file serving

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Caching Configuration - Redis for production
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'), # Configure in .env or use default Redis URL
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer', ],
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser', ],
    'DEFAULT_THROTTLE_CLASSES': [ # Rate limiting for API - adjust as needed
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/minute', # Example: 200 requests per minute for anonymous users
        'user': '1000/minute' # Example: 1000 requests per minute for authenticated users
    }
}

# Logging Configuration - Production Grade Logging to Files
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'engine_log_file': {
            'level': 'INFO', # Or 'DEBUG' for more detail in development
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'engine.log'), # Log file path
            'formatter': 'verbose'
        },
        'webapp_log_file': {
            'level': 'INFO', # Or 'DEBUG' for more detail in development
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'webapp.log'), # Log file path
            'formatter': 'verbose'
        },
        'console': { # Optional console handler for development
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'engine': { # Logger for engine components
            'handlers': ['engine_log_file', 'console'], # Or just ['engine_log_file'] in production
            'level': 'INFO',
            'propagate': False,
        },
        'webapp': { # Logger for webapp components
            'handlers': ['webapp_log_file', 'console'], # Or just ['webapp_log_file'] in production
            'level': 'INFO',
            'propagate': False,
        },
        'django': { # Default Django logger - you can customize handlers if needed
            'handlers': ['console'], # Or your preferred Django log handlers
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Whitenoise settings - for serving static files efficiently in production
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False