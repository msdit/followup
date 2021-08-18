from datetime import timedelta

DEBUG = True

TIME_ZONE = "Asia/Tehran"

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "followup_db",
        "USER": "msdit",
        "PASSWORD": "m1481225",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
