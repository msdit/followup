from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class FollowUpUserManager(UserManager):
    pass


class User(AbstractUser):
    email = models.EmailField("Email Address", unique=True)
    email_password = models.CharField("Email Password", max_length=128)
    imap_server = models.CharField(
        "IMAP Server", max_length=128, default="outlook.office365.com"
    )
    imap_port = models.IntegerField("IMAP Server", default="993")
    smtp_server = models.CharField(
        "SMTP Server", max_length=128, default="smtp.office365.com"
    )
    smtp_port = models.IntegerField("SMTP Server", default="587")

    REQUIRED_FIELDS = ["username", "email_password"]
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]

    objects = FollowUpUserManager
