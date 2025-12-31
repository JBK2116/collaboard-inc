"""
This module stores utility functions used throughout the application
"""

from .authentication.models import CustomUser


def user_exists(email: str) -> bool:
    """
    Checks if a user exists with the given email
    :param email: Email of the user
    :return: True if the user exists, otherwise False
    """
    return CustomUser.objects.filter(email=email).exists()
