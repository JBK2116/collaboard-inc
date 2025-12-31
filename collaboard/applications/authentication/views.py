from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..authentication import services
from ..utils import user_exists
from .forms import SignupForm

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
    if request.method == "POST":
        form = SignupForm(request.POST)
        # validate initial form data
        if not form.is_valid():
            return render(
                request=request,
                template_name="authentication/signup.html",
                context={
                    "form": form,
                    "email_exists": False,
                    "email_sent_error": False,
                },
            )
        # ensure no matching user with same email
        if user_exists(form.cleaned_data["email"]):
            return render(
                request=request,
                template_name="authentication/signup.html",
                context={"email_exists": True, "form": form, "email_sent_error": False},
            )
        # generate the email verification token and send it
        email_verification_token: str = services.generate_account_verification_token(
            form.cleaned_data["email"],
            make_password(form.cleaned_data["password1"]),
            form.cleaned_data["first_name"],
            form.cleaned_data["last_name"],
        )
        if not services.send_account_verification_email(
            email_verification_token, form.cleaned_data["email"], request
        ):
            return render(
                request=request,
                template_name="authentication/signup.html",
                context={"email_exists": False, "form": form, "email_sent_error": True},
            )
        # email was sent by now
        return render(
            request=request,
            template_name="authentication/verify_account_email_sent.html",
            context={"email": form.cleaned_data["email"]},
        )

    return render(
        request=request,
        template_name="authentication/signup.html",
        context={
            "form": SignupForm(),
            "email_exists": False,
            "email_sent_error": False,
        },
    )


# TODO: Implement this
def verify_email(request: HttpRequest) -> HttpResponse:
    pass
