import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
DEBUG = True
#DEBUG = os.environ.get('MYDEBUG', False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'MYSECRET', '78cdsvc7sdavb07nvar87ynbdravs7by87yvb7ab09se7vybrsd7vyd9'
    )

PG_HOST = os.environ.get('PG_HOST', 'postgres-server')
PG_USER = os.environ.get('PG_USER', 'postgres')
PG_PASSWORD = os.environ.get('PG_PASSWORD', 'newsjota')
PG_DATABASE = os.environ.get('PG_DATABASE', 'dbnewsjota')
PG_PORT = os.environ.get('PG_PORT', '5432')

RBMQ_HOST = os.environ.get('RBMQ_HOST', 'broker-server')
RBMQ_PORT = os.environ.get('RBMQ_PORT', '5672')
RBMQ_USER = os.environ.get('RBMQ_USER', 'guest')
RBMQ_PASS = os.environ.get('RBMQ_PASS', 'guest')
BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost:5672')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')


#ALLOWED_HOSTS =os.environ.get('ALLOWED_HOSTS').split(',')
ALLOWED_HOSTS = ['*']
# Application definition
INSTALLED_APPS = [
    #Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libs
    'rest_framework.apps.RestFrameworkConfig',
    # Apps
    'news.apps.NewsConfig',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# LOGIN / LOGOUT
LOGIN_REDIRECT_URL = 'backend'
LOGOUT_REDIRECT_URL = 'frontend'

#LOGIN_REDIRECT_URL = '/'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'http://localhost']

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PG_DATABASE,
        'USER': PG_USER,
        'PASSWORD': PG_PASSWORD,
        'HOST': PG_HOST,
        'PORT': PG_PORT,
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000 # Define um tamanho maior, se necessário.
DATA_UPLOAD_MAX_MEMORY_SIZE = 6242880 

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'