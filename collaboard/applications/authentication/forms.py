"""
This module stores all authentication forms used throughout this application
"""

from typing import Any

from django import forms

from .models import CustomUser


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=128, required=True, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        max_length=128, required=True, widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]

    def clean_password2(self) -> Any:
        """
        Custom clean method.
        Primarily used to ensure that password1 and password2
        are equal.
        """
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(message="Passwords don't match")
        return password2
