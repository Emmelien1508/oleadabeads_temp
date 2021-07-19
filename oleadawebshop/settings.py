from pathlib import Path
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'hpwptazjkxg%t1#b6)xldod5t9p43-+8%&j3qmx1zk!#s4$gnh'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'oleadabeads.herokuapp.com', 'oleadabeads.nl', 'https://oleadabeads-383i7.ondigitalocean.app/']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webshop.apps.WebshopConfig',
    'crispy_forms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'oleadawebshop.urls'

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
                'webshop.context_processors.add_variable_to_context'
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'oleadawebshop.wsgi.application'

SESSION_ENGINE = 'webshop.session_backend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/usr/local/bin/my.cnf',
        },
    }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

DATE_INPUT_FORMATS = (
    '%d %B %Y'
)

DATE_FORMAT = 'j F Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'j F Y H:i'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'j F'
SHORT_DATE_FORMAT = 'j N Y'
SHORT_DATETIME_FORMAT = 'j N Y H:i'
FIRST_DAY_OF_WEEK = 1

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = ''
MEDIA_ROOT = os.path.join(BASE_DIR, 'webshop/static/')

AUTH_USER_MODEL = 'webshop.Customer'
AUTHENTICATION_BACKENDS = ['webshop.backends.EmailBackend']
LOGIN_REDIRECT_URL = ('..')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'oleadabeads@gmail.com'
EMAIL_HOST_PASSWORD = 'iCleem1998'
EMAIL_USE_TLS = True