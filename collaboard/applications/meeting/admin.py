from django.contrib import admin

from .models import Meeting, MeetingStatistics, Question, Response

# Register your models here.
admin.site.register(Meeting)
admin.site.register(MeetingStatistics)
admin.site.register(Question)
admin.site.register(Response)
