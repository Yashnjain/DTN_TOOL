"""
Django settings for price_tracker project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""




from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l$kow)o6x(=#lukeqr-x7)z)@dkozrm4s#nwyyfhq^&@e#21gx'

# SECURITY WARNING: don't run with debug turned on in production!
#dev
# DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition



INSTALLED_APPS = [
   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft',
    'app',
    
]


MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'price_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]


WSGI_APPLICATION = 'price_tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Local
# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
#  }



# Prod ENV
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ['DBNAME'],
#         'HOST': os.environ['DBHOST'],
#         'USER': os.environ['DBUSER'],
#         'PASSWORD': os.environ['DBPASS'],
#         'CONN_MAX_AGE' : 600
#     }
# }





# Prod Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dtnprice-database',
        'HOST': 'bio-dtn.postgres.database.azure.com',
        'USER': 'biodtnadmin01',
        'PASSWORD': 'wVRZP7mfd78*gRChPDgVbQf@cavP',
        'CONN_MAX_AGE': 600
    }
}





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




# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'US/Central'

# TIME_ZONE = 'UTC-5'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]




SOCIALACCOUNT_PROVIDERS = {
     'microsoft': {
          'TENANT': 'biourja.com',
     }
}


SITE_ID = 1


#django-allauth registraion settings
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
  
# 1 day
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 
  
#or any other page
ACCOUNT_LOGOUT_REDIRECT_URL ='/accounts/microsoft/login' 
  
# redirects to profile page if not configured.
LOGIN_REDIRECT_URL = "/"


#79609b7e-ea0f-4917-82b0-379bd49bffa2    - value 
#Ak48Q~Vg-vKD5-JwYaR1jjFqAA4S80nXyoMsTbdS  -secret key

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-mail.outlook.com'
# EMAIL_HOST_USER = "itdevsupport@biourja.com"
EMAIL_HOST_USER = "prism.support@biourja.com"
# EMAIL_HOST_PASSWORD = "Z@^>Nzh'x85]@dL?"
EMAIL_HOST_PASSWORD = "Chirag0987"

ACCOUNT_EMAIL_VERIFICATION = "none"

DATA_UPLOAD_MAX_MEMORY_SIZE = 100000000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000000






#dev
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
STATICFILES_DIRS = [
    BASE_DIR,"static"
]
STATIC_URL = 'static/'
DEBUG = True



#prod
# CSRF_TRUSTED_ORIGINS = ["https://dtnpriceupload.azurewebsites.net"]
# CSRF_COOKIE_SECURE = False
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER =('HTTP_X_FORWARDED_PROTO','https')
# SOCIALACCOUNT_AUTO_SIGNUP = False
# DEBUG = False
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')




MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,"media")



#File_prod
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(os.environ['HOME'], 'site', 'wwwroot', 'media')





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'sql.log',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}







