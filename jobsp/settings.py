import os
import dj_database_url

from celery.schedules import crontab
from corsheaders.defaults import default_headers, default_methods
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes", "on")
TEMPLATE_DEBUG = DEBUG

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "peeljobs@micropyramid.com")


PEEL_URL = os.getenv("PEEL_URL", "http://peeljobs.com/")

# Celery configuration with REDIS_URL support and fallback
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL:
    try:
        # Test Redis connection for Celery
        import redis
        client = redis.from_url(REDIS_URL)
        client.ping()  # Test connection
        
        # Use REDIS_URL if available (for platforms like Render, Heroku, etc.)
        CELERY_BROKER_URL = REDIS_URL
        CELERY_RESULT_BACKEND = REDIS_URL
        print(f"✅ Celery Redis broker configured successfully")
    except Exception as e:
        print(f"⚠️ Celery Redis connection failed ({e}), using local fallback")
        # Fallback to local Redis or disable Celery in production
        CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
        CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
        # In production without Redis, we can use database backend
        if not DEBUG:
            CELERY_TASK_ALWAYS_EAGER = True  # Execute tasks synchronously
            CELERY_TASK_EAGER_PROPAGATES = True
else:
    # Fallback to CELERY_BROKER_URL or default for local development
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_IMPORTS = ("dashboard.tasks")


# Enable debug logging

logging = "DEBUG"

GIT_APP_ID = os.getenv("GITAPPID")
GIT_APP_SECRET = os.getenv("GITAPPSECRET")

ALLOWED_HOSTS = ["peeljobs.com", "test.peeljobs.com", "localhost", "127.0.0.1", "opensource-job-portal-1.onrender.com"]

# tw app
tw_oauth_token_secret = os.getenv("twoauthtokensecret")
tw_oauth_token = os.getenv("twoauthtokensecret")

TW_APP_KEY = os.getenv("TWAPPKEY")
TW_APP_SECRET = os.getenv("TWAPPSECRET")
OAUTH_TOKEN = os.getenv("OAUTHTOKEN")
OAUTH_SECRET = os.getenv("OAUTHSECRET")

PJ_TW_APP_KEY = os.getenv("PJTWAPPKEY")
PJ_TW_APP_SECRET = os.getenv("PJTWAPPSECRET")

# fb app
FB_APP_ID = os.getenv("FACEBOOK_APP_ID")
FB_SECRET = os.getenv("FACEBOOK_APP_SECRET")
FB_PEELJOBS_PAGEID = os.getenv("FBPEELJOBSPAGEID")

# google app
GOOGLE_CLIENT_ID = GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_LOGIN_HOST = os.getenv("GOOGLE_LOGIN_HOST")

# ln app
LN_API_KEY = os.getenv("LNAPIKEY")
LN_SECRET_KEY = os.getenv("LNSECRETKEY")
LN_OAUTH_USER_TOKEN = os.getenv("LNOAUTHUSERTOKEN")
LN_OAUTH_USER_SECRET = os.getenv("LNOAUTHUSERSECRET")
LN_COMPANYID = os.getenv("LNCOMPANYID")

# re-captcha
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
RECAPTCHA_USE_SSL = True

# Make this unique, and don"t share it with anybody.
SECRET_KEY = os.getenv("SECRET_KEY")

ADMINS = (
    # ("Your Name", "your_email@example.com"),
)

MANAGERS = ADMINS

# Database configuration with DATABASE_URL support
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Use DATABASE_URL if available (for platforms like Render, Heroku, etc.)
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL)
    }
else:
    # Fallback to individual environment variables for local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }


TIME_ZONE = "Asia/Kolkata"

LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False


# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "compressor.finders.CompressorFinder",
)

HTML_MINIFY = os.getenv("HTML_MINIFY", False)

ROOT_URLCONF = "jobsp.urls"

# Python dotted path to the WSGI application used by Django"s runserver.
WSGI_APPLICATION = "jobsp.wsgi.application"

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.messages",
    "sorl.thumbnail",
    "compressor",
    "storages",
    "peeldb",
    # 'django_simple_forum',
    "haystack",
    "dashboard",
    "search",
    # "simple_pagination",
    "django_celery_beat",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django_ses",
)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # "hmin.middleware.MinMiddleware",
    # "hmin.middleware.MarkMiddleware",
    # "jobsp.middlewares.DetectMobileBrowser",
    "jobsp.middlewares.LowerCased",
]


CORS_ALLOWED_ORIGINS = ["http://localhost:4200", "http://127.0.0.1:4200"]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.peeljobs\.com$",
]
CORS_ALLOW_METHODS = list(default_methods)
CORS_ALLOW_HEADERS = list(default_headers)


AUTH_USER_MODEL = "peeldb.User"
LOGIN_URL = "/"

AUTHENTICATION_BACKENDS = (
    "social.auth_backend.PasswordlessAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR + "/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "jobsp.context_processors.export_vars",
                "peeldb.context_processors.get_pj_icons",
            ],
        },
    },
]

AM_ACCESS_KEY = AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AM_PASS_KEY = AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_SES_REGION_NAME = os.getenv("AWS_SES_REGION_NAME")
AWS_SES_REGION_ENDPOINT = os.getenv("AWS_SES_REGION_ENDPOINT")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")


COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_REBUILD_TIMEOUT = 5400


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"
COMPRESS_OUTPUT_DIR = "CACHE"
COMPRESS_URL = STATIC_URL
COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ("text/less", "lessc {infile} {outfile}"),
    ("text/x-sass", "sass {infile} {outfile}"),
    ("text/x-scss", "sass {infile} {outfile}"),
)

COMPRESS_OFFLINE_CONTEXT = {
    "STATIC_URL": "STATIC_URL",
}

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


# Haystack settings for Elasticsearch
# HAYSTACK_CONNECTIONS = {
#     "default": {
#         "ENGINE": "peeldb.backends.ConfigurableElasticSearchEngine",
#         "URL": "http://127.0.0.1:9200/",
#         "INDEX_NAME": "job_haystack",
#         "TIMEOUT": 60,
#     },
# }

# Elasticsearch configuration with environment variable support
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://127.0.0.1:9200/")

if os.getenv("ELASTICSEARCH_URL") or DEBUG:
    # Use Elasticsearch when URL is provided or in development
    HAYSTACK_CONNECTIONS = {
        "default": {
            "ENGINE": "haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine",
            "URL": ELASTICSEARCH_URL,
            "INDEX_NAME": "haystack",
        },
    }
else:
    # Use simple backend for production when Elasticsearch is not available
    HAYSTACK_CONNECTIONS = {
        "default": {
            "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
        },
    }


HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"
HAYSTACK_DEFAULT_OPERATOR = "OR"
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 1

CELERY_TIMEZONE = "Asia/Calcutta"

CELERY_BEAT_SCHEDULE = {
    # Executes every day evening at 5:00 PM GMT +5.30
    "moving-published-jobs-to-live": {
        "task": "dashboard.tasks.jobpost_published",
        "schedule": crontab(minute="*", day_of_week="mon,tue,wed,thu,fri,sat"),
    },
    "sending-today-applied-users-info-to-recruiters": {
        "task": "dashboard.tasks.recruiter_jobpost_applicants",
        "schedule": crontab(
            hour="16", minute="00", day_of_week="mon,tue,wed,thu,fri,sat"
        ),
    },
    # "sending-profile_update-notifications-to-applicants": {
    #     "task": "dashboard.tasks.applicants_notifications",
    #     "schedule": crontab(
    #         hour="16", minute="00", day_of_week="mon,tue,wed,thu,fri,sat"
    #     ),
    # },
    "sending-daily-statistics-report-to-admins": {
        "task": "dashboard.tasks.daily_report",
        "schedule": crontab(
            hour="08", minute="00", day_of_week="mon,tue,wed,thu,fri,sat,sun"
        ),
    },
    "sending-weekly-jobs-notifications-to-applicants": {
        "task": "dashboard.tasks.applicants_job_notifications",
        "schedule": crontab(hour="09", minute="00", day_of_week="mon"),
    },
    # "all-users-profile-update-and-birthday-notifications": {
    #     "task": "dashboard.tasks.alerting_applicants",
    #     "schedule": crontab(
    #         hour="10", minute="05", day_of_week="mon,tue,wed,thu,fri,sat,sun"
    #     ),
    # },
    # "alerting-all-inactive-users-and-applicants-resume-upload-notifications": {
    #     "task": "dashboard.tasks.applicants_profile_update_notifications",
    #     "schedule": crontab(
    #         hour="09", minute="00", day_of_week="mon,tue,wed,thu,fri,sat,sun"
    #     ),
    # },
    "sending-profile-update-notifications-two-hours-after-registering": {
        "task": "dashboard.tasks.applicants_profile_update_notifications_two_hours",
        "schedule": crontab(
            hour="*/2", minute="00", day_of_week="mon,tue,wed,thu,fri,sat,sun"
        ),
    },
    # "walkin-notifications-to-applicants": {
    #     "task": "dashboard.tasks.applicants_walkin_job_notifications",
    #     "schedule": crontab(hour="09", minute="00", day_of_week="thu"),
    # },
    "daily-sitemap-generation": {
        "task": "dashboard.tasks.sitemap_generation",
        "schedule": crontab(
            hour="00", minute="10", day_of_week="mon,tue,wed,thu,fri,sat"
        ),
    },
    "sending-today-live-jobs-to-users-based-on-profile": {
        "task": "dashboard.tasks.job_alerts_to_users",
        "schedule": crontab(
            hour="17", minute="00", day_of_week="mon,tue,wed,thu,fri,sat,sun"
        ),
    },
    "sending-today-live-jobs-to-alerts": {
        "task": "dashboard.tasks.job_alerts_to_alerts",
        "schedule": crontab(
            hour="10", minute="00", day_of_week="mon,tue,wed,thu,fri,sat,sun"
        ),
    },
    "sending-today-live-jobs-to-subscribers": {
        "task": "dashboard.tasks.job_alerts_to_subscribers",
        "schedule": crontab(
            hour="18", minute="00", day_of_week="mon,tue,wed,thu,fri,sat,sun"
        ),
    },
    # "recruiter-profile-update-notifications": {
    #     "task": "dashboard.tasks.recruiter_profile_update_notifications",
    #     "schedule": crontab(hour="09", minute="30", day_of_week="mon"),
    # },
    "haystack-rebuilding-indexes": {
        "task": "dashboard.tasks.rebuilding_index",
        "schedule": crontab(
            hour="00", minute="20", day_of_week="mon,tue,wed,thu,fri,sat,sun"
        ),
    },
}
SUPPORT_EMAILS = [
    "ashwin@micropyramid.com",
]


THUMBNAIL_COLORSPACE = None
THUMBNAIL_PRESERVE_FORMAT = False
THUMBNAIL_FORMAT = "PNG"
THUMBNAIL_CACHE_TIMEOUT = 3600 * 24 * 365 * 10

TIMEZONE = "Asia/Calcutta"
LOGO = "http://localhost:8000/logo.png"


THUMBNAIL_BACKEND = "jobsp.thumbnailname.SEOThumbnailBackend"
THUMBNAIL_DEBUG = True

THUMBNAIL_FORCE_OVERWRITE = True



# AWS_ENABLED = os.getenv("AWSENABLED")
# DISQUS_SHORTNAME = ""

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
#         "LOCATION": "127.0.0.1:11211",
#         "TIMEOUT": 48 * 60 * 60,
#         "OPTIONS": {"server_max_value_length": 1024 * 1024 * 2,},
#     }
# }

# Cache configuration with Redis support and fallback
if REDIS_URL:
    try:
        # Test Redis connection before using it
        import redis
        client = redis.from_url(REDIS_URL)
        client.ping()  # Test connection
        
        # Use Redis cache with REDIS_URL (for production)
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": REDIS_URL,
                "TIMEOUT": 48 * 60 * 60,
                "OPTIONS": {
                    "CONNECTION_POOL_KWARGS": {
                        "retry_on_timeout": True,
                        "socket_keepalive": True,
                        "socket_keepalive_options": {},
                    }
                }
            }
        }
        print(f"✅ Redis cache configured successfully")
    except Exception as e:
        print(f"⚠️ Redis connection failed ({e}), falling back to local memory cache")
        # Fallback to local memory cache if Redis fails
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache", 
                "LOCATION": "unique-snowflake",
                "TIMEOUT": 48 * 60 * 60,
            }
        }
else:
    # Use local memory cache for development (if no Redis)
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
            "TIMEOUT": 48 * 60 * 60,
        }
    }

FB_ACCESS_TOKEN = os.getenv("FBACCESSTOKEN")
FB_PAGE_ACCESS_TOKEN = os.getenv("FBPAGEACCESSTOKEN")
FB_GROUP_ACCESS_TOKEN = os.getenv("FBGROUPACCESSTOKEN")
FB_ALL_GROUPS_TOKEN = os.getenv("FBALLGROUPSTOKEN")
FB_DEL_ACCESS_TOKEN = os.getenv("FBDELACCESSTOKEN")
REC_FB_ACCESS_TOKEN = os.getenv("RECFBACCESSTOKEN")

URLS = [
    "http://stage.peeljobs.com/",
    "http://stage.peeljobs.com/fresher-jobs/",
    "http://stage.peeljobs.com/jobs/",
    "http://stage.peeljobs.com/companies/",
]

DAILY_REPORT_USERS = [
    "kamal.seo@gmail.com",
    "varun@micropyramid.com",
    "ashwin@micropyramid.com",
]
# MIDDLEWARE_CLASSES = MIDDLEWARE

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        # 'rest_framework.authentication.SessionAuthentication',
    ]
}

REST_USE_JWT = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

EMAIL_BACKEND = "django_ses.SESBackend"

MP_CELERY_MONITOR_KEY = os.getenv("MP_CELERY_MONITOR_KEY")
CELERY_MONITOR_URL = os.getenv("CELERY_MONITOR_URL")

# Tailwind CSS Configuration
TAILWIND_CSS_FILE = "css/tailwind-output.css"

# Try to load local settings for development only
if DEBUG and not DATABASE_URL:  # Only load local settings in debug mode and when not using DATABASE_URL
    try:
        from .settings_local import *
        print("Local development settings loaded")
    except ImportError:
        pass  # settings_local.py doesn't exist or has import errors
