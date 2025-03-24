import os
from pathlib import Path
import dj_database_url
import environ
import logging


def configure_production_security():
    SECURE_HSTS_SECONDS = 3600  # 1 hora
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializa environ
env = environ.Env(
    MYSECRET=(str, '78cdsvc7sdavb07nvar87ynbdravs7by87yvb7ab09se7vybrsd7vyd9'),
    DATABASE_URL=(str, 'postgres://postgres:postgres@localhost:5432/postgres'),
    
    RABBITMQ_URL=(str, 'amqp://guest:guest@localhost:5672/'),
    EXCHANGE_NEWS=(str, 'jota_news_exchange'),

    QUEUE_NEWS_INCOMING=(str, 'source_receiver'),
    QUEUE_NEWS_CLASSIFICATION=(str, 'source_classification'),
    QUEUE_NEWS_URGENCY=(str, 'new_notification'),
    
    ROUTING_KEY_INCOMING=(str, 'source.incoming'),
    ROUTING_KEY_CLASSIFICATION=(str, 'source.preprocess'),
    ROUTING_KEY_NOTIFICATION=(str, 'new.classification')
)
# Lê variáveis do arquivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env.local'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('MYSECRET')


# Inicializa o ambiente (pode ser 'development', 'production', etc.)
ENVIRONMENT = env('ENVIRONMENT', default='development')

# Configura o logging com base no ambiente
if ENVIRONMENT == 'development':
    logging.basicConfig(level=logging.DEBUG)
elif ENVIRONMENT == 'production':
    logging.basicConfig(level=logging.INFO)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='your-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)


#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '.jota.info']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # apps terceiros
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'drf_yasg',

    # Apps locais
    'news_app',
    
    # Metricas
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_permissions_policy.PermissionsPolicyMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'core_dj.urls'

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

WSGI_APPLICATION = 'core_dj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL'),
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'pt-br'
LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Onde você vai armazenar os arquivos .po e .mo
]
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

if not DEBUG:
    CORS_ALLOWED_ORIGINS += [
        'https://jota.info',
        'https://www.jota.info',
    ]
    # Segurança no ambiente de produção
    configure_production_security()



PROMETHEUS_LATENCY_BUCKETS = (0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 25.0, 50.0, 75.0, float("inf"),)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'django_cache'),
    }
}


RABBITMQ_URL=env('RABBITMQ_URL', default='amqp://jota_user:jota_password@rabbitmq:5672/')
EXCHANGE_NEWS=env('EXCHANGE_NEWS',default='jota_news_exchange')

QUEUE_NEWS_INCOMING=env('QUEUE_NEWS_INCOMING',default='source_incoming')
QUEUE_NEWS_CLASSIFICATION=env('QUEUE_NEWS_CLASSIFICATION',default='source_classification')
QUEUE_NEWS_URGENCY=env('QUEUE_NEWS_URGENCY',default='urgent_notification')

ROUTING_KEY_INCOMING=env('ROUTING_KEY_INCOMING', default='source.incoming')
ROUTING_KEY_CLASSIFICATION=env('ROUTING_KEY_CLASSIFICATION',default='source.classification')
ROUTING_KEY_NOTIFICATION=env('ROUTING_KEY_NOTIFICATION',default='urgent.notification')

