"""
Django settings for trishartsy project.
Final Production Version for Vercel + Neon + Cloudinary.
"""

from pathlib import Path
import os
import dj_database_url

# ===============================
# BASE DIRECTORY
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY SETTINGS
# ===============================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!=*ng+x2sh#wioas^d2s%%q=eh#q+829&hl$43+9($($u14&fj')

# DEBUG should be False in production
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

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
    
    # Must be above cloudinary_storage
    'django.contrib.staticfiles',
    
    # Third-party
    'cloudinary_storage',
    'cloudinary',

    # Local apps
    'booking',
]


# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
                'django.contrib.messages.context_processors.messages', # Fixed typo here
                'django.template.context_processors.media',
                'booking.context_processors.latest_booking_context',
            ],
        },
    },
]


# ===============================
# DATABASE (Neon PostgreSQL)
# ===============================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# ===============================
# CLOUDINARY STORAGE CONFIG
# ===============================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}


# ===============================
# STATIC & MEDIA FILES
# ===============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "booking" / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ===============================
# AUTHENTICATION
# ===============================
AUTH_USER_MODEL = 'booking.CustomUser'
LOGIN_URL = '/login/'


# ===============================
# INTERNATIONALIZATION
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'