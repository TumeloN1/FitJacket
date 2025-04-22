from pathlib import Path
import os
from dotenv import load_dotenv
import mongoengine

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "keys.env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-secure-fitjacketteam2")
DEBUG = True
ALLOWED_HOSTS = []

# databases and middleware
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'workouts',
    'goals',
    'accounts',
    'dashboard',
    'adminpanel',
    'home',
    'social',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# url, templates, backends
ROOT_URLCONF = 'FitJacket.urls'
WSGI_APPLICATION = 'FitJacket.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'FitJacket' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.csrf'
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    'accounts.auth_backends.MongoEngineBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# mongoengine
MONGO_DB_NAME   = 'FitJacketDatabase'
MONGO_ATLAS_URI = os.getenv(
    'MONGO_ATLAS_URI',
    'mongodb+srv://fitjacketteam2:bmZQ1y5FerkHVHuw@fitjacket.hktnt3w.mongodb.net/FitJacketDatabase?retryWrites=true&w=majority&tls=true&appName=FitJacket'
)


mongoengine.connect(db=MONGO_DB_NAME, host=MONGO_ATLAS_URI)

#just some validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

STATIC_URL        = '/static/'
STATICFILES_DIRS  = [BASE_DIR / 'FitJacket' / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EXERCISESDB_API_KEY = os.getenv("EXERCISESDB_API_KEY")
