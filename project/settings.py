import os
from configparser import ConfigParser
from celery.schedules import crontab
from kombu import Queue

config = ConfigParser()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Build Info
try:
    with open(os.path.join(BASE_DIR, 'build', 'BUILD_INFO'), 'r') as build_info:
        PROJECT_VERSION = build_info.readline().strip()
        PROJECT_NAME = build_info.readline().strip()
except IOError as e:
    PROJECT_VERSION = '0.0.0'
    PROJECT_NAME = 'project'

prod_config_path = os.path.join(f'/etc/{PROJECT_NAME}/{PROJECT_NAME}.conf')
local_config_path = os.path.join(BASE_DIR, 'build', 'conf', 'local.conf')

config_path = prod_config_path if os.path.exists(prod_config_path) else local_config_path
config.read(config_path)

DEBUG = config.getboolean('main', 'DEBUG')
SECRET_KEY = config.get('main', 'SECRET')
PROJECT_URL = config.get('main', 'URL')
LOG_FILE = config.get('main', 'LOG_FILE')

INTERNAL_IPS = ['127.0.0.1']
ALLOWED_HOSTS = ['*']


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
]

if DEBUG:
    DJANGO_APPS += ['debug_toolbar']

PROJECT_APPS = [
    'core',
    'accounts',
    'posts',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEBUG_TOOLBAR_PANELS = []

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

ROOT_URLCONF = 'project.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'debug': DEBUG
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'ENGINE'),
        'NAME': config.get('database', 'NAME'),
        'USER': config.get('database', 'USER'),
        'PASSWORD': config.get('database', 'PASSWORD'),
        'HOST': config.get('database', 'HOST'),
        'PORT': config.getint('database', 'PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    },
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

LOGIN_REDIRECT_URL = 'posts:picture_list'
AUTH_USER_MODEL = 'accounts.User'

AUTH_MODEL_BACKEND = 'django.contrib.auth.backends.ModelBackend'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
]

SOCIAL_AUTH_REDIRECT_IS_HTTPS = not DEBUG

SOCIAL_AUTH_VK_OAUTH2_KEY = config.get('oauth', 'VK_ID')
SOCIAL_AUTH_VK_OAUTH2_SECRET = config.get('oauth', 'VK_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['wall', ]
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['bdate', ]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'accounts.pipeline.update_posts_on_create',
)

IMAGE_RANK_WEIGHTS_PATH = config.get('image_rank', 'WEIGHTS_PATH')

VKAPI_ACCESS_TOKEN = config.get('vkapi', 'ACCESS_TOKEN')
VKAPI_VERSION = config.get('vkapi', 'VERSION')

CELERY_BROKER_URL = config.get('celery', 'BROKER_URL')
CELERY_RESULT_BACKEND = config.get('celery', 'RESULT_BACKEND')

CELERY_RESULT_EXPIRES = 7 * 24 * 60 * 60
CELERY_SEND_EVENTS = True
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = 'default'

CELERY_TASK_QUEUES = [
    Queue('default'),
]

CELERY_BEAT_SCHEDULE = {
    'payment_monitor': {
        'task': 'posts.tasks.update_all',
        'schedule': crontab(minute='0', hour='2'),
    }
}
