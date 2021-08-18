from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = "utils"
        abstract = True
