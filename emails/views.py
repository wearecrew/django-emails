from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render

from .constants import HTML


def double_preview(request, ctype_id, obj_id):
    return render(
        request,
        "emails/double_preview.html",
        {"obj_id": obj_id, "ctype_id": ctype_id},
    )


def preview(request, ctype_id, obj_id, mode):
    model_class = ContentType.objects.get_for_id(ctype_id).model_class()
    obj = model_class.objects.get(id=obj_id)
    if mode == HTML:
        content = obj.preview_html
    else:
        content = obj.preview_text
    return HttpResponse(content)
