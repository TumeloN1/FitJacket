from pathlib import Path
import os
import mongoengine as db
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-oe)+a7y6&afed9%+758ctns5=he4ff9)y$otp$fc#uhq3$4tmp'
DEBUG = True
ALLOWED_HOSTS = []

MONGO_DB_NAME = 'FitJacketDatabase'
MONGO_ATLAS_URI = os.environ.get(
    'MONGO_ATLAS_URI',
    'mongodb+srv://fitjacketteam2:bmZQ1y5FerkHVHuw@fitjacket.hktnt3w.mongodb.net/FitJacketDatabase?retryWrites=true&w=majority'
)

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

ROOT_URLCONF = 'FitJacket.urls'

AUTHENTICATION_BACKENDS = [
    'accounts.auth_backends.MongoEngineBackend',
    'django.contrib.auth.backends.ModelBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'FitJacket', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FitJacket.wsgi.application'



'''
mongodb+srv://fitjacketteam2:bmZQ1y5FerkHVHuw@fitjacket.hktnt3w.mongodb.net/?retryWrites=true&w=majority&appName=FitJacket

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://fitjacketteam2:bmZQ1y5FerkHVHuw@fitjacket.hktnt3w.mongodb.net/?appName=FitJacket"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
'''


db.connect(db=MONGO_DB_NAME, host=MONGO_ATLAS_URI)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'FitJacket', 'static')]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EXERCISESDB_API_KEY = os.environ.get('EXERCISEDB_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def connect_to_mongo():
    db.connect(db=MONGO_DB_NAME, host=MONGO_ATLAS_URI)
