from datetime import timedelta

SECRET_KEY = "vqo&=1w*g@rn2=r(g@@!q6q2m6o1k@62@#p@!x^el_9q@f5wl5"
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
