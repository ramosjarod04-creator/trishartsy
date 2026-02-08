"""
Django settings for trishartsy project.
Modified for Vercel Deployment.
"""

from pathlib import Path
import os

# ===============================
# BASE DIRECTORY
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY SETTINGS
# ===============================
# Use an environment variable for the secret key in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!=*ng+x2sh#wioas^d2s%%q=eh#q+829&hl$43+9($($u14&fj')

# DEBUG should be False in production
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Allow Vercel domains and local development
ALLOWED_HOSTS = ['.vercel.app', 'now.sh', 'localhost', '127.0.0.1']


# ===============================
# APPLICATIONS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'booking',
]


# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# URLS & WSGI
# ===============================
ROOT_URLCONF = 'trishartsy.urls'
WSGI_APPLICATION = 'trishartsy.wsgi.application'


# ===============================
# TEMPLATES
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.messages',
                'django.template.context_processors.media',
                'booking.context_processors.latest_booking_context',
            ],
        },
    },
]


# ===============================
# DATABASE
# ===============================
# Note: SQLite will reset on every Vercel deployment. 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===============================
# PASSWORD VALIDATION
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===============================
# INTERNATIONALIZATION
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True


# ===============================
# STATIC & MEDIA FILES
# ===============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "booking" / "static",
]
# Critical for production:
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ===============================
# AUTHENTICATION
# ===============================
AUTH_USER_MODEL = 'booking.CustomUser'
LOGIN_URL = '/login/'


# ===============================
# DEFAULT PRIMARY KEY FIELD TYPE
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'