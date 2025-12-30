from typing import Any

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.urls import path, reverse_lazy

from ..authentication import views

# TODO: Add paths for verifying user email after signup attempt
urlpatterns: list[Any] = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/forgot-password.html",
            email_template_name="authentication/forgot-password-email.html",
            html_email_template_name="authentication/forgot-password-email.html",
            success_url=reverse_lazy("password_reset_done"),
            form_class=PasswordResetForm,
        ),
        name="password_reset",
    ),  # handles sending the password reset email
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/forgot-password.html",
            extra_context={"email_sent": True},
        ),
        name="password_reset_done",
    ),  # handles showing the password reset email sent page
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/reset-password.html",
            form_class=SetPasswordForm,
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/login.html",
            extra_context={"password_reset_done": True},
        ),
        name="password_reset_complete",
    ),
]
