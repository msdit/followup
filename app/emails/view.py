import datetime

from django.db.models import (
    Q,
    Max,
    Min,
    OuterRef,
    Exists,
)
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.utils import timezone
from django.template import Template, Context

from emails.models import Contact, FollowUpEmailsTemplate, SentMail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from imap_tools import MailBox, OR
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

# Create your views here.


@login_required
def send_email_view(request, sent_mail_id):
    email = SentMail.objects.filter(id=sent_mail_id, sent=False)
    if not email.exists():
        return HttpResponseNotFound("email not found")

    user = request.user
    host = user.smtp_server
    port = user.smtp_port
    username = user.email
    password = user.email_password
    try:
        email = email.first()
        backend = EmailBackend(
            host=host,
            port=port,
            password=password,
            username=username,
            use_tls=True,
        )

        mail = EmailMessage(
            subject=email.generated_subject,
            body=email.generated_text,
            from_email=username,
            to=[email.contact.email],
            connection=backend,
        )
        mail.content_subtype = "html"
        mail.send()
        return HttpResponseRedirect("/")

    except Exception as _error:
        return HttpResponseBadRequest("Error in sending mail >> {}".format(_error))


@login_required
def contact_info_view(request, contact_id):
    contact = Contact.objects.filter(id=contact_id)
    if not contact.exists():
        return HttpResponseNotFound("contact not found")
    contact = contact.first()

    emails = SentMail.objects.filter(contact=contact)
    print(contact, emails)
    return render(request, "contact_info.html", {"contact": contact, "emails": emails})


@login_required
def home_view(request):
    user = request.user
    not_comunicated = list(
        Contact.objects.filter(in_comunication=False, is_active=True).values_list(
            "email", flat=True
        )
    )

    if len(not_comunicated) > 0:
        # UPDATE LIST
        mailbox = MailBox(host=user.imap_server, port=user.imap_port).login(
            user.email, user.email_password
        )
        new_answers = list(
            set([msg.from_ for msg in mailbox.fetch(OR(from_=not_comunicated))])
        )
        mailbox.logout()
        Contact.objects.filter(email__in=new_answers).update(in_comunication=True)

    # FIND TODAY EMAILS
    first_template = FollowUpEmailsTemplate.objects.get(
        is_active=True,
        index=(
            FollowUpEmailsTemplate.objects.filter(is_active=True).aggregate(
                min=Min("index")
            )["min"]
        ),
    )
    last_template_id = FollowUpEmailsTemplate.objects.filter(is_active=True).aggregate(
        max=Max("index")
    )["max"]

    new_contact_list = Contact.objects.filter(
        in_comunication=False, is_active=True, sent_mails__isnull=True
    )

    SentMail.objects.bulk_create(
        [
            SentMail(
                contact=c,
                template=first_template,
                generated_text=Template(first_template.email).render(
                    Context(c.__dict__)
                ),
                generated_subject=Template(first_template.subject).render(
                    Context(c.__dict__)
                ),
            )
            for c in new_contact_list
        ]
    )

    new_followup_contact_list = (
        Contact.objects.filter(
            in_comunication=False,
            is_active=True,
        )
        .filter(
            ~Q(sent_mails__template__id=last_template_id)
            & ~Exists(SentMail.objects.filter(Q(sent=False), contact=OuterRef("pk")))
        )
        .distinct("email")
    )

    def find_next_template(user):
        print(
            user,
            SentMail.objects.filter(contact=user).aggregate(max=Max("template__index"))[
                "max"
            ],
        )
        last_sent_template = SentMail.objects.get(
            contact=user,
            template__index=(
                SentMail.objects.filter(contact=user).aggregate(
                    max=Max("template__index")
                )["max"]
            ),
        )

        next_template = FollowUpEmailsTemplate.objects.get(
            is_active=True,
            index=(
                FollowUpEmailsTemplate.objects.filter(
                    is_active=True, index__gt=last_sent_template.template.index
                ).aggregate(min=Min("index"))["min"]
            ),
        )

        return {
            "contact": user,
            "template": next_template,
            "available_to_send": last_sent_template.sent_date.date()
            + datetime.timedelta(days=next_template.days_after_prev),
            "generated_text": Template(next_template.email).render(
                Context(user.__dict__)
            ),
            "generated_subject": Template(next_template.subject).render(
                Context(user.__dict__)
            ),
        }

    SentMail.objects.bulk_create(
        [SentMail(**find_next_template(c)) for c in new_followup_contact_list]
    )

    new_emails = SentMail.objects.filter(
        sent=False, available_to_send__lte=timezone.now()
    )

    not_responsed = SentMail.objects.filter(sent=True, template__id=last_template_id)

    return render(
        request, "home.html", {"new_emails": new_emails, "not_responsed": not_responsed}
    )
