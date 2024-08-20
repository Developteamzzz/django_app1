"""
Django settings for cproject project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# APPEND_SLASH = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hfg5w$)@voa9cbw^r&$cl94eh^p3ra0nn_o_rgf*jb7o%&ay6m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Configure email backend (replace with your SMTP settings)
# Email settings


# SMTP server settings
# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Correct SMTP server address for Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cihsdteam@gmail.com'
EMAIL_HOST_PASSWORD = 'pwfiwnmkwjpwutle'  # Replace 'your_password' with the actual password for 'cihsdteam@gmail.com'
# SMTP servaer settings
    
ALLOWED_HOSTS = []
    

# Application definition
# settings.py

# Use database for session storage (default)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Session cookie age (in seconds)
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# Whether to use a secure cookie for the session
SESSION_COOKIE_SECURE = True

# HTTPOnly flag for the session cookie
SESSION_COOKIE_HTTPONLY = True

# Whether the session expires when the user closes the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_section.capp',
    'main_section.mainapp',
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

ROOT_URLCONF = 'cproject.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'admin_section','templates'),
                 os.path.join(BASE_DIR,'main_section','templates'),
                 ],
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

WSGI_APPLICATION = 'cproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'cluster',
        'HOST':'localhost',
        'USER':'root',
        'PASSWORD':'',
        'PORT':'3306',
        'OPTIONS':{
          'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
    }      
   }
}  

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(BASE_DIR.joinpath('admin_section', 'static')),
    str(BASE_DIR.joinpath('main_section', 'static')),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'admin_section', 'media')
os.path.join(BASE_DIR, 'main_section', 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


INTERNAL_IPS = [
    "127.0.0.1",
]



