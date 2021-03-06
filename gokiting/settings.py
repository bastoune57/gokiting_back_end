"""
Django settings for gokiting project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s84+)z^xpqlxg2)37udm3f7m1p2q6ce$8w78tg33is(c17_86z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'gokiting.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'instructors', # my app
    'locations', # my app
    'languages', # my app
    'categories', # my app
    'rest_framework', # framework to generate REST API
    'corsheaders', # to check connexions origin
    'drf_yasg', # framework to generate REST API documentation
    'django_filters', # drf url filtering
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #"whitenoise.middleware.WhiteNoiseMiddleware", # whote noise forr static files handling
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'gokiting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'gokiting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',#sqlite3',
#         'USER': 'yryreekh',#'yryreekh',#xwiunijy',
#         'PASSWORD': 'rOxpogZWCwPO42d4enpFoN4GaWNQ6yA1',#'rOxpogZWCwPO42d4enpFoN4GaWNQ6yA1',#'TCHU88rY3gsIY2Zggc3JljLJAhjcOuPw',
#         'NAME': 'yryreekh',#'yryreekh', #'xwiunijy',
#         # 'USER': 'xwiunijy',
#         # 'PASSWORD': 'TCHU88rY3gsIY2Zggc3JljLJAhjcOuPw',
#         # 'NAME': 'xwiunijy',
#         'HOST': 'surus.db.elephantsql.com',
#         'PORT': '5432',
#     }
# }

# TEST DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',#sqlite3',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'NAME': 'gokiting',
        'HOST': 'db',#'192.168.1.12',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# for white noise
STATIC_ROOT = BASE_DIR / "static"

# https://www.devhandbook.com/django/user-profile/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Directory where uploaded media is saved.
MEDIA_URL = '/media/' # Public URL at the browser

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # https://www.geeksforgeeks.org/adding-pagination-in-apis-django-rest-framework/
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    #'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

CORS_ORIGIN_ALLOW_ALL = True

# https://docs.djangoproject.com/fr/4.0/topics/auth/customizing/
AUTH_USER_MODEL = 'instructors.User'

# logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}