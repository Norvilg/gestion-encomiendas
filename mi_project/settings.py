"""
Django settings for mi_project project.
"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')


# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del proyecto
    'envios',
    'clientes',
    'rutas',
]


# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'mi_project.urls'


# TEMPLATES
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
                'django.contrib.messages.context_processors.messages',

                # Context processor personalizado
                #'envios.context_processors.estadisticas_globales',
            ],
        },
    },
]


WSGI_APPLICATION = 'mi_project.wsgi.application'


# DATABASE (POSTGRESQL)
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}


# PASSWORD VALIDATION
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


# INTERNATIONALIZATION
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True


# STATIC FILES
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# AUTH
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# SESSIONS (personalización del sistema de login)

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# La sesión NO se cierra al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Duración de la sesión: 8 horas
SESSION_COOKIE_AGE = 60 * 60 * 8

# Solo HTTPS en producción (déjalo en False en desarrollo)
SESSION_COOKIE_SECURE = False

# Nombre personalizado de la cookie
SESSION_COOKIE_NAME = 'encomiendas_session'