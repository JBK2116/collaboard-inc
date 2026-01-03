import logging
from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from ..authentication import services
from ..utils import user_exists
from .forms import LoginForm, SignupForm
from .models import CustomUser

# TODO: Add rate limiting to these views via `django-ratelimit` package

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignupForm(request.POST)
        # validate initial form data
        if not form.is_valid():
            logger.log(
                level=logging.INFO,
                msg="Invalid Signup Form",
                extra={"reasons": f"{form.errors}"},
            )
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
            logger.log(
                level=logging.INFO,
                msg="Invalid Signup Form",
                extra={"reasons": f"Email {form.cleaned_data} already exists"},
            )
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
        logger.log(
            level=logging.INFO,
            msg="Email Verification Sent",
            extra={"email": form.cleaned_data["email"]},
        )
        return render(
            request=request,
            template_name="authentication/verify_account_email_sent.html",
            context={"email": form.cleaned_data["email"]},
        )
    else:
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(
            request=request,
            template_name="authentication/signup.html",
            context={
                "form": SignupForm(),
                "email_exists": False,
                "email_sent_error": False,
            },
        )


@require_http_methods(["GET"])
def verify_email(request: HttpRequest) -> HttpResponse:
    token: str | None = request.GET.get("token")
    if not token:
        logger.log(level=logging.WARNING, msg="Email Verification Token Not Found")
        return render(
            request=request,
            template_name="authentication/email_verified.html",
            context={"email_verified": False},
        )
    payload: dict[str, Any] | None = services.verify_account_verification_token(
        token
    )  # also handles logging error
    if payload is None:
        return render(
            request=request,
            template_name="authentication/email_verified.html",
            context={"email_verified": False},
        )
    # email is verified by now
    new_user: CustomUser = CustomUser(
        email=payload["email"],
        first_name=payload["first_name"],
        last_name=payload["last_name"],
    )
    new_user.password = payload["password"]
    new_user.save()
    logger.log(level=logging.INFO, msg="User Created", extra={"user": new_user})
    return render(
        request=request,
        template_name="authentication/email_verified.html",
        context={"email_verified": True},
    )


@require_http_methods(["GET", "POST"])
def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: LoginForm = LoginForm(request.POST)
        if not form.is_valid():
            logger.log(
                level=logging.INFO,
                msg="Invalid Login Form",
                extra={"reasons": f"{form.errors}"},
            )
            return render(
                request=request,
                template_name="authentication/login.html",
                context={
                    "form": form,
                    "password_reset_done": False,
                    "invalid_email_password": False,
                },
            )
        # form is valid by now
        user: CustomUser | None = authenticate(
            email=form.cleaned_data["email"], password=form.cleaned_data["password"]
        )
        if user is None:
            logger.log(
                level=logging.INFO,
                msg="Invalid Login Form",
                extra={"reasons": f"Email: {form.cleaned_data['email']} not found"},
            )
            return render(
                request=request,
                template_name="authentication/login.html",
                context={
                    "form": form,
                    "password_reset_done": False,
                    "invalid_email_password": True,
                },
            )
        # user is authenticated by now
        login(request, user)
        if request.POST.get("remember_me"):
            request.session.set_expiry(services.SESSION_EXPIRY_SECONDS)
        else:
            request.session.set_expiry(0)  # expire on browser close
        logger.log(level=logging.INFO, msg="User Logged In", extra={"user": user})
        return redirect("dashboard")
    else:
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(
            request=request,
            template_name="authentication/login.html",
            context={
                "password_reset_done": False,
                "invalid_email_password": False,
                "form": LoginForm(),
            },
        )
