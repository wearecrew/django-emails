import logging

from django.dispatch import receiver

from anymail.signals import tracking

from .models import Email, Event

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@receiver(tracking)
def handle_event(sender, event, esp_name, **kwargs):
    try:
        email = Email.objects.get(message_id=event.message_id)
    except Email.DoesNotExist:
        logger.error("Email with message_id %s does not exist", event.message_id)
        return

    Event.objects.create(event_type=event.event_type, email=email)
