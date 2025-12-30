from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def landing(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="index.html", context={})


def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="dashboard.html", context={})
