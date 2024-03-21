from django.urls import path

from . import views
from .constants import HTML, TEXT

urlpatterns = [
    path(
        "preview/<int:ctype_id>/<int:obj_id>/",
        views.double_preview,
        name="double_preview",
    ),
    path(
        "preview/<int:ctype_id>/<int:obj_id>/html/",
        views.preview,
        name="preview",
        kwargs={"mode": HTML},
    ),
    path(
        "preview/<int:ctype_id>/<int:obj_id>/text/",
        views.preview,
        name="preview",
        kwargs={"mode": TEXT},
    ),
]
