from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from django_object_actions import DjangoObjectActions, action

from . import models
from .filters import DeliveredFilter
from .tasks import resend_email


class EventInline(admin.TabularInline):
    readonly_fields = ["event_type"]
    model = models.Event
    extra = 0


@admin.register(models.Email)
class EmailAdmin(DjangoObjectActions, admin.ModelAdmin):
    inlines = [EventInline]
    list_display = ["subject", "to_email", "created_at", "delivered"]
    search_fields = ["to_email"]
    list_filter = ["sent_at", DeliveredFilter]
    change_actions = ["resend"]

    def get_queryset(self, request):
        return super().get_queryset(request).with_delivered()

    @admin.display(description="Delivered")
    def delivered(self, obj):
        return obj.delivered

    delivered.admin_order_field = "delivered"

    @action(label="Resend", description="Resend email")
    def resend(self, request, obj):
        resend_email(obj.id)
        messages.add_message(request, messages.INFO, "Email resent")
        return HttpResponseRedirect(reverse("admin:emails_email_changelist"))

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        context.update(
            {
                "show_save": True,
                "show_save_and_continue": True,
                "show_save_and_add_another": False,
                "show_delete": False,
            }
        )
        return super().render_change_form(request, context, add, change, form_url, obj)


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = models.EmailTemplate
        fields = "__all__"


@admin.register(models.EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    form = EmailTemplateForm
