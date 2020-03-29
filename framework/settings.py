import os
from environs import Env

from datetime import timedelta

env = Env()
env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret key used to generate session tokens, password reset tokens etc.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='@v(sr0a1eocvp9x=pndj(ff*ll_d2yn7e&t19t!%$(bx47brrl')
# Sets whether debug mode is activated. If true, errors logs are publicly visible instead of error pages
DEBUG = env.bool('DEBUG', default=True)
# Lists the hosts where the app is allowed to run. Set to '*' (any) on default
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Plugins
    'corsheaders',
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',

    # functionality apps
    'media',
    'taxonomy',
    'user',
    'list'
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

ROOT_URLCONF = 'framework.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

CORS_ORIGIN_ALLOW_ALL = True
WSGI_APPLICATION = 'framework.wsgi.application'

#
# DATABASE SETTINGS
#
# whether to use postgres db, as set in environment
if env.bool('USE_PGDB', default=False):
    print(env.str('POSTGRES_HOST'))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.str('POSTGRES_DB'),
            'USER': env.str('POSTGRES_USER'),
            'PASSWORD': env.str('POSTGRES_PASSWORD'),
            'HOST': env.str('POSTGRES_HOST'),
            'PORT': '5432',
        }
    }
# uses simple sqlite3 database
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Static & Media Files Settings
if env.bool('USE_S3', default=False):
    AWS_ACCESS_KEY_ID = env.str('S3_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env.str('S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env.str('S3_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # Static Files
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'framework.utils.storage.StaticStorage'

    # # Public Media
    # PUBLIC_MEDIA_LOCATION = 'media/public'
    # MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    # DEFAULT_FILE_STORAGE = 'framework.helpers.storage.PublicMediaStorage'
    #
    # # User Media
    # USER_MEDIA_LOCATION = 'media/user'
    # USER_FILE_STORAGE = 'framework.helpers.storage.UserMediaStorage'
else:
    STATIC_ROOT = ''
    STATIC_URL = '/static/'
    MEDIA_URL = '/'

# List of static file directories
STATICFILES_DIRS = (os.path.join('static'),)
# Maximum allowed upload size  for any file
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 25


#
# Authentication
#
if 'user' in INSTALLED_APPS:
    AUTH_USER_MODEL = 'user.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
    'framework.utils.auth.AuthEmailBackend'
]

#
# Internationalization
#
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True


#
# GraphQL Settings
#
GRAPHENE = {
    'SCHEMA': 'framework.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

GRAPHQL_JWT = {
    'JWT_ALLOW_ARGUMENT': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_USER_LOGGED_IN_SIGNAL': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}