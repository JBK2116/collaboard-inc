from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def landing(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="index.html", context={})


def login(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name="authentication/login.html",
        context={"password_reset_done": False, "invalid_email_password": False},
    )


def signup(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name="authentication/signup.html",
        context={
            "email_exists": False,
        },
    )
