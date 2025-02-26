from pathlib import Path
import os
import dj_database_url
import cloudinary
cloudinary.config(secure=True)
if os.path.isfile('env.py'):
    import env

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

SECRET_KEY = os.environ.get("SECRET_KEY")


#------------ Security check -------------- #

DEBUG = True

ALLOWED_HOSTS = ['localhost',
                '8000-philippeits-cipasseport-ueridz1s5o8.ws-eu118.gitpod.io',
                 '.herokuapp.com',]

CSRF_TRUSTED_ORIGINS = [
    "https://*.codeinstitute-ide.net/",
    "https://*.herokuapp.com",
    "https://8000-philippeits-cipasseport-ueridz1s5o8.ws-eu117.gitpod.io",
]


#------------ Apps and so on -------------- #

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_summernote',
    'cloudinary',
    'pet_businesses',
    'pet_owners',
    'vouchers',
    'grpd',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'my_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'my_project.wsgi.application'


#------------ Apps and so on -------------- #

DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}



#------------ Authentification -------------- #

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none' #Instead of mandatory
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_SIGNUP_FORM_CLASS = 'pet_businesses.forms.CustomSignupForm'


#------------ Internatlisation -------------- #

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
