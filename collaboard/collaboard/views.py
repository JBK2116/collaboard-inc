from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def landing(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="index.html", context={})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="dashboard.html", context={})
