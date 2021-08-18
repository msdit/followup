from django.urls import path
from .view import home_view, send_email_view, contact_info_view

urlpatterns = [
    path("", home_view, name="home"),
    path("send_email/<int:sent_mail_id>", send_email_view, name="send_email"),
    path("contact_info/<int:contact_id>", contact_info_view, name="contact_info"),
]
