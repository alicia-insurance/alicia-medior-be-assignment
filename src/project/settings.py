import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "your_secret_key"

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "url_shortener",
    "drf_yasg",  # Swagger documentation
    "corsheaders",  # CORS headers for API
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "project.middleware.logging_middleware.APILoggingMiddleware",  # Custom logging middleware
]

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "project.utils.throttles.CustomBurstThrottle",  # Custom throttle for burst requests
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "50/minute",  # unauthenticated users
        "user": "50/minute",  # authenticated users
        "burst": "50/minute",  # burst requests
    },
}

SWAGGER_SETTINGS = {
    # 'SECURITY_DEFINITIONS': {
    #     'Token': {
    #         'type': 'apiKey',
    #         'name': 'Authorization',
    #         'in': 'header'
    #     },
    # },
    "USE_SESSION_AUTH": False  # Disable session authentication for Swagger
}

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME", "dev_db"),
        "USER": os.environ.get("DB_USER", "dev_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "dev_password"),
        "HOST": os.environ.get("DB_HOST", "172.22.0.11"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # 'redis' is the Docker service name
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} [{filename}:{lineno}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "django.log"),
            "formatter": "verbose",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "errors.log"),
            "level": "ERROR",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file", "error_file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "url_shortener": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "project.middleware.logging_middleware": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
