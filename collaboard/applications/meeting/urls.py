from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_meeting, name="create_meeting"),
    path("locked/", views.locked_meeting, name="locked_meeting"),
    path("ended/", views.end_meeting_participant, name="end_meeting"),
    path("<uuid:meeting_id>/host/", views.host_meeting, name="host_meeting"),
]
