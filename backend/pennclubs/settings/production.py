import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from pennclubs.settings.base import *  # noqa: F401, F403
from pennclubs.settings.base import BACKEND_DOMAIN, DATABASES, FRONTEND_DOMAIN


DEBUG = False

# Fix MySQL Emoji support
DATABASES["default"]["OPTIONS"] = {"charset": "utf8mb4"}

# Honour the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow production host headers
ALLOWED_HOSTS = [BACKEND_DOMAIN]

# Make sure SECRET_KEY is set to a secret in production
SECRET_KEY = os.environ.get("SECRET_KEY", None)

# Sentry settings
SENTRY_URL = os.environ.get("SENTRY_URL", "")
sentry_sdk.init(dsn=SENTRY_URL, integrations=[DjangoIntegration()])

# DLA settings
PLATFORM_ACCOUNTS = {
    "REDIRECT_URI": f"https://{BACKEND_DOMAIN}/accounts/callback/",
    "ADMIN_PERMISSION": "clubs_admin",
}

###############################################################
# SETTINGS TO ALLOW FRONTEND TO MAKE AJAX REQUESTS TO BACKEND #
###############################################################
# DO NOT USE IF DJANGO APP IS STANDALONE
# Django CORS Settings
CORS_ORIGIN_WHITELIST = [f"https://www.{FRONTEND_DOMAIN}", f"https://{FRONTEND_DOMAIN}"]

CSRF_TRUSTED_ORIGINS = [f"www.{FRONTEND_DOMAIN}", FRONTEND_DOMAIN]


# Email client information
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_USE_TLS = True

# Upload file storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_ACCESS_SECRET_ID = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
