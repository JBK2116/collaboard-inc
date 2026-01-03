import uuid

from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

from ..authentication.models import CustomUser


# Create your models here.
class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    access_code = models.CharField(
        null=False,
        blank=False,
        validators=[MinLengthValidator(8), MaxLengthValidator(8)],
        help_text="The access code for participants to join the meeting",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="meetings",
        null=False,
        help_text="The user that created the meeting",
    )
    title = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        help_text="The title of the meeting",
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        null=False,
        default="No description provided",
        help_text="The description of the meeting",
    )
    duration = models.IntegerField(
        default=60,
        null=False,
        blank=False,
        help_text="The duration of the meeting in minutes",
        validators=[
            MaxValueValidator(60),
            MinValueValidator(1),
        ],  # TODO: Update this to 5 minutes later for PROD
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user}"


class MeetingStatistics(models.Model):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name="statistics", null=False
    )
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats for {self.meeting.title}"


class Question(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="questions",
        null=False,
        help_text="The meeting that the question belongs to",
    )
    text = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        help_text="the question text",
    )
    index = models.PositiveIntegerField(
        null=False, blank=False, help_text="The index of the question in the meeting"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]  # First 50 chars


class Response(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="responses",
        null=False,
        help_text="The question that the response belongs to",
    )
    text = models.CharField(
        max_length=500, blank=False, null=False, help_text="The response text"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response to: {self.question.text[:30]}"
