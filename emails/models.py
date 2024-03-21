import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from .managers import EmailManager

logger = logging.getLogger(__name__)


class EmailTemplate(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    text_template = models.TextField()
    html_template = models.TextField()
    preview_data = models.JSONField(null=True, blank=True)

    @property
    def preview_text(self):
        context = Context(self.preview_data or {})
        template = Template(self.text_template)
        content = template.render(context)
        return render_to_string("emails/preview_text.html", {"content": content})

    @property
    def preview_html(self):
        context = Context(self.preview_data or {})
        template = Template(self.html_template)
        return template.render(context)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        ctype_id = ContentType.objects.get_for_model(self).id
        return reverse("double_preview", kwargs={"ctype_id": ctype_id, "obj_id": self.id})


class Email(models.Model):
    class Meta:
        ordering = ["-created_at"]

    from_email = models.CharField(max_length=255)
    to_email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    text_content = models.TextField()
    html_content = models.TextField()
    message_id = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    metadata = models.TextField(blank=True)
    data = models.JSONField(null=True, blank=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.PROTECT)

    objects = EmailManager()

    def get_absolute_url(self):
        ctype_id = ContentType.objects.get_for_model(self).id
        return reverse("double_preview", kwargs={"ctype_id": ctype_id, "obj_id": self.id})

    def __str__(self):
        return f"{self.subject} | {self.to_email}"

    @property
    def preview_text(self):
        return render_to_string("emails/preview_text.html", {"content": self.text_content})

    @property
    def preview_html(self):
        return self.html_content

    @staticmethod
    def render_template(template_str, data):
        template = Template(template_str)
        context = Context(data)
        return template.render(context)

    def send(self, attachments=[]):
        self.sent_at = timezone.now()
        try:
            message = EmailMultiAlternatives(
                subject=self.subject,
                body=self.text_content,
                from_email=self.from_email,
                to=[self.to_email],
                attachments=attachments,
            )
            message.attach_alternative(self.html_content, "text/html")
            message.send()
            if settings.ENV == "production":
                self.message_id = message.anymail_status.message_id

        except Exception as exc:
            self.metadata = str(exc)
            logger.error("Could not send message %s", self.id)
        self.save()


class Event(models.Model):
    class EventType(models.TextChoices):
        QUEUED = "queued"
        SENT = "sent"
        REJECTED = "rejected"
        FAILED = "failed"
        BOUNCED = "bounced"
        DEFERRED = "deferred"
        DELIVERED = "delivered"
        OPENED = "opened"
        CLICKED = "clicked"
        UNKNOWN = "unknown"

    event_type = models.CharField(max_length=255, choices=EventType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
