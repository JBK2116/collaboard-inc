from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_meeting, name="create_meeting"),
]
