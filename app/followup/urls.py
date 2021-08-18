from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Follow Up Panel"
admin.site.site_title = "FOLLOW UP"
admin.site.index_title = "Admin Panel"

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("", include("emails.urls")),
]
