"""
This module stores the business logic to be used in `views.py`
"""

import os
from typing import Any

from django.conf import settings
from django.core import signing
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.template.loader import render_to_string

EXPIRATION_SECONDS = 60 * 60 * 24  # 24 Hours
SESSION_EXPIRY_SECONDS = 60 * 60 * 24 * 7 * 2  # 2 weeks
EXPIRATION_HOURS = 24  # MUST MATCH `EXPIRATION_SECONDS`

SALT = os.getenv("VERIFICATION_EMAIL_SALT")
if not SALT:
    raise ImproperlyConfigured("Set the VERIFICATION_EMAIL_SALT environment variable")


def generate_account_verification_token(
    email: str, password: str, first_name: str, last_name: str
) -> str:
    """
    Generates an account verification token for the user
    :param email: Raw user email
    :param password: Hashed user password
    :param first_name: First name of user
    :param last_name: Last name of user
    :return: Verification token
    """
    return signing.dumps(
        {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
        salt=SALT,
    )


def verify_account_verification_token(token: str) -> dict[str, Any] | None:
    """
    Validates an account verification token
    :param token: Token to verify
    :return: user email if token is valid, else None
    """
    try:
        payload: dict[str, Any] = signing.loads(
            token, salt=SALT, max_age=EXPIRATION_SECONDS
        )
        return payload
    except (signing.BadSignature, signing.SignatureExpired):
        return None  # token was tampered with or just expired


def send_account_verification_email(
    token: str, user_email: str, request: HttpRequest
) -> bool:
    """
    Sends a verification email to the provided user email

    :param token: Token to embed in the email
    :param user_email: Email to send to
    :param request: Http request
    :returns: True if the email was successfully sent, else false
    """
    protocol: str = "https" if request.is_secure() else "http"
    domain: str = request.get_host()
    subject: str = "Collaboard - Verify Your Account"
    text_content: str = "Verify your account to begin using Collaboard"
    html_message = render_to_string(
        template_name="emails/verify_account_email.html",
        context={
            "token": token,
            "protocol": protocol,
            "domain": domain,
            "hours": EXPIRATION_HOURS,
        },
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_FROM_USER,
        to=[user_email],
    )
    msg.attach_alternative(content=html_message, mimetype="text/html")
    # noinspection PyBroadException
    try:
        msg.send()
        return True
    except Exception as e:
        print(e.args)
        return False
