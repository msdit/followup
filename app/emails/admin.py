from django.contrib import admin

from .models import FollowUpEmailsTemplate, Contact, SentMail


@admin.register(FollowUpEmailsTemplate)
class FollowUpEmailsTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "is_active",
        "index",
        "email",
    )
    list_filter = ("is_active",)
    search_fields = (
        "email",
        "subject",
    )
    readonly_fields = (
        "created_date",
        "last_modified_date",
    )
    ordering = ("index",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "email",
        "is_active",
        "in_comunication",
        "region",
        "country",
        "contact",
        "company",
        "location",
        "achivment",
    )
    search_fields = (
        "client",
        "email",
        "region",
        "country",
        "contact",
        "company",
        "location",
        "achivment",
    )
    list_filter = (
        "region",
        "country",
        "in_comunication",
        "is_active",
    )
    readonly_fields = ("created_date", "last_modified_date", "in_comunication")
    ordering = ("-created_date",)


@admin.register(SentMail)
class SentMailAdmin(admin.ModelAdmin):
    list_display = (
        "contact",
        "generated_subject",
        "sent",
        "sent_date",
        "available_to_send",
    )
    list_filter = ("sent",)
    search_fields = (
        "generated_text",
        "contact__client",
        "contact__email",
        "contact__region",
        "contact__country",
        "contact__contact",
        "contact__company",
        "contact__location",
        "contact__achivment",
    )
    raw_id_fields = (
        "contact",
        "template",
    )
    readonly_fields = (
        "generated_subject",
        "generated_text",
        "created_date",
    )
    ordering = ("-created_date",)
