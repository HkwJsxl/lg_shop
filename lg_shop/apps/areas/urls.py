from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.AreasView.as_view(), name="areas"),
]
