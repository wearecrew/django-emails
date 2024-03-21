from django.db import models


class EmailQuerySet(models.QuerySet):
    def with_delivered(self):
        return self.annotate(
            delivered=models.Count("event", filter=models.Q(event__event_type="delivered"))
        )


class EmailManager(models.Manager):
    def create(self, **obj_data):
        email_template = obj_data["template"]
        data = obj_data["data"]
        obj_data.update(
            {
                "text_content": self.model.render_template(email_template.text_template, data),
                "html_content": self.model.render_template(email_template.html_template, data),
                "subject": email_template.subject,
            }
        )
        return super().create(**obj_data)

    def get_queryset(self):
        return EmailQuerySet(self.model, using=self._db)

    def with_delivered(self):
        return self.get_queryset().with_delivered()
