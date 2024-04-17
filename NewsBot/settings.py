import os
from pathlib import Path

from environ import Env

from NewsBot.loguru_django import LoguruInterceptHandler


BASE_DIR = Path(__file__).resolve().parent.parent

env = Env(
    DEBUG=(bool, False)
)
env.read_env(Path(BASE_DIR, '.env'))

SECRET_KEY = env.str('SECRET_KEY')

TG_TOKEN_BOT = env.str('TG_TOKEN_BOT')

REDIS_URL = env('REDIS_URL')

DEBUG = env.bool('DEBUG')

DEFAULT_PAGINATION_BOT = 5

ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS',
    default=[
        '127.0.0.1', 'localhost'
    ]
)

CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=[
        'http://127.0.0.1:8080'
    ]
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'news',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NewsBot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsBot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': env.db_url('DATABASE_URL'),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'Ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'loguru_console': {
            '()': LoguruInterceptHandler,
            'level': 1,
        },
    },
    'loggers': {
        '': {
            'handlers': ['loguru_console'],
            'level': "INFO",
            'propagate': True,
        },
        'django.server': {
            'handlers': ['loguru_console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['loguru_console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['loguru_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['loguru_console'],
    },
}
