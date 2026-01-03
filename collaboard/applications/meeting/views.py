# Create your views here.
import json
import logging
from typing import Any

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..meeting import services
from .models import Meeting, Question

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def create_meeting(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data: dict[str, Any] = json.loads(request.body)
        new_meeting: Meeting | None = services.create_meeting(
            request.user,
            data.get("title"),
            data.get("description"),
            data.get("duration"),
        )
        if new_meeting is None:
            logger.log(level=logging.INFO, msg="Meeting Creation Failed")
            return JsonResponse(status=400, data={})
        new_questions: list[Question] | None = services.create_questions(
            new_meeting, data.get("questions")
        )
        if new_questions is None:
            logger.log(level=logging.INFO, msg="Questions Creation Failed")
            return JsonResponse(status=400, data={})
        new_meeting.save()
        logger.log(
            level=logging.INFO,
            msg="Meeting Creation Successful",
            extra={"meeting": new_meeting},
        )
        for q in new_questions:
            q.save()
        logger.log(
            level=logging.INFO,
            msg="Questions Creation Successful",
            extra={"questions": new_questions},
        )
        return JsonResponse(data={}, status=200)
    else:
        return render(
            request=request, template_name="meeting/create_meeting.html", context={}
        )


@require_http_methods(["GET"])
def locked_meeting(request: HttpRequest) -> HttpResponse:
    return render(
        request=request, template_name="meeting/locked_meeting.html", context={}
    )


@require_http_methods(["GET"])
def end_meeting_participant(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="meeting/end_meeting.html", context={})


@login_required
@require_http_methods(["GET"])
def host_meeting(request: HttpRequest) -> HttpResponse:
    return render(
        request=request, template_name="meeting/host_meeting.html", context={}
    )
