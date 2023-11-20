"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yonk%@m2qu=-o75y+dml%z^%8n6la^!)3#vba1g#84v4*=*7h)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Некоторые соцсети не перенарпавляют на 'localhost', '127.0.0.1'
# В файл C:\Windows\System32\Drivers\etc\hosts прописать 127.0.0.1 mysite.com
ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1', '14b1-212-58-120-42.ngrok-free.app']

# для Ngrok
CSRF_TRUSTED_ORIGINS = ['https://14b1-212-58-120-42.ngrok-free.app']

# Задаём URL для модели
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sorl.thumbnail',
    'social_django',
    'jquery.apps.JqueryConfig',

    # Для коректной отправки имейлов, через админку можно поменять домен сайта
    'django.contrib.sites',
    'images.apps.ImagesConfig',

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

ROOT_URLCONF = 'bookmarks.urls'

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

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# указывает адрес, куда Django будет перенаправлять польз. при успешной авторизации, если не указан GET-параметр next
LOGIN_REDIRECTED_URL = 'dashboard'
# адрес, куда нужно перенаправлять пользователя для входа в систему, например из обработчиков с декоратором login_required;
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# Emails settings
# Разрешить доступ к почтовому ящику с помощью почтовых клиентов
# С сервера imap.yandex.ru по протоколу IMAP
# Способ авторизации по IMAP
# Пароли приложений и OAuth-токены

# Создать пароль приложения EMAIL_HOST_PASSWORD = ...

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'bfaroon@yandex.ru'
EMAIL_HOST_PASSWORD = 'bmapekwfxpyblwek'
# EMAIL_PASSWORD = '123qweQ.'

# Емейл отправителя, будет подставляться в поле атправителя
FROM_EMAIL = "bfaroon@yandex.ru"
# Емуйл администратора, для отправки администратору
EMAIL_ADMIN = "bfaroon@yandex.ru"

#  !!!!!!!!!!!!!!!!!!!!!!!!              DEFAULT_FROM_EMAIL  = "bfaroon@yandex.ru"       'django.contrib.sites',
DEFAULT_FROM_EMAIL = "bfaroon@yandex.ru"

SITE_ID = 1

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# сойт по востановлению пароля
# https://proghunter.ru/articles/django-base-2023-password-recovery-form

# Для вывода имейлов в консоль
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Сервис временной электронной почты
# https://temp-mail.org/ru/

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
]

 # Аутентификация Facebook
SOCIAL_AUTH_FACEBOOK_KEY = '254013034325367'
SOCIAL_AUTH_FACEBOOK_SECRET = '58ae974465b7a98812123174e3916221'
#Мы можем указать, какие данные хотим запрашивать из Facebook-аккаунта. Для этого нужно задать настройку
# SOCIAL_AUTH_FACEBOOK_SCOPE с дополнительными правами, которые будут запрошены у пользователя при попытке авторизации
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
