from background_task import background


@background()
def resend_email(email_id):
    from .models import Email

    email = Email.objects.get(id=email_id)
    email.pk = None
    email.save()
    email.send()
