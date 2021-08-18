from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    add_form_template = "admin/change_form.html"
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Email info",
            {
                "fields": (
                    "email",
                    "email_password",
                    "imap_server",
                    "imap_port",
                    "smtp_server",
                    "smtp_port",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("last_login", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "email_password",
                    "first_name",
                    "last_name",
                    "password",
                ),
            },
        ),
    )
    list_filter = (
        "is_active",
        "groups",
    )
