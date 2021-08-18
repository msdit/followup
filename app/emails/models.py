from django.core.validators import MinValueValidator
from utils.models import BaseModel
from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone


class FollowUpEmailsTemplate(BaseModel):
    is_active = models.BooleanField(default=True)
    index = models.IntegerField(
        unique=True, validators=[MinValueValidator(1)], help_text="min: 1"
    )
    subject = models.CharField(
        max_length=255,
        help_text="You can use: {{client}}, {{email}}, {{region}}, {{country}}, {{contact}}, {{company}}, {{location}}, {{achivment}}",
    )
    days_after_prev = models.IntegerField(default=0)
    email = RichTextField(
        help_text="You can use: {{client}}, {{email}}, {{region}}, {{country}}, {{contact}}, {{company}}, {{location}}, {{achivment}}"
    )

    def __str__(self):
        return f"follow up email No. {self.index} ({self.subject})"

    class Meta:
        app_label = "emails"


class Contact(BaseModel):
    is_active = models.BooleanField(default=True)
    client = models.CharField(max_length=512, blank=True, default="")
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=512, blank=True, default="")
    country = models.CharField(max_length=512, blank=True, default="")
    contact = models.CharField(max_length=512, blank=True, default="")
    company = models.CharField(max_length=512, blank=True, default="")
    location = models.CharField(max_length=512, blank=True, default="")
    achivment = models.CharField(max_length=512, blank=True, default="")
    in_comunication = models.BooleanField(default=False)

    def __str__(self):
        return self.client

    class Meta:
        app_label = "emails"


class SentMail(BaseModel):
    sent = models.BooleanField(default=False)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="sent_mails"
    )
    template = models.ForeignKey(
        FollowUpEmailsTemplate, on_delete=models.CASCADE, related_name="sent_mails"
    )
    generated_subject = models.CharField(
        max_length=255, default="", null=True, blank=True
    )
    generated_text = RichTextField()

    available_to_send = models.DateTimeField(default=timezone.now)

    sent_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.contact} - {self.template}"

    class Meta:
        app_label = "emails"
