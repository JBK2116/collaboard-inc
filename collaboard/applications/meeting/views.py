# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
def create_meeting(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)  # Just want to see the received data
        return JsonResponse(data={"message": "ok"}, status=200)
    return render(
        request=request, template_name="meeting/create_meeting.html", context={}
    )
