# accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


# ================= REQUEST OTP FORM =================

class RequestOTPForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control border-warning',
            'placeholder': 'Enter Email'
        })
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control border-warning',
            'placeholder': 'Enter Mobile Number'
        })
    )

    role = forms.ChoiceField(
        choices=(
            ('client', 'Client'),
            ('lawyer', 'Lawyer'),
        ),
        widget=forms.Select(attrs={
            'class': 'form-control border-warning'
        })
    )


# ================= CREATE ACCOUNT FORM =================

class CreateAccountForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border-warning'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-warning'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-warning'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


# ================= RESET PASSWORD FORM =================

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-warning'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-warning'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
