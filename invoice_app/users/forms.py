from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django import forms

User = get_user_model()

PROVINCES = [
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MB', 'Manitoba')
]


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields["login"].label = ""
        self.fields["password"].label = ""
        self.fields["remember"].widget.attrs.update({
            "name": "checkbox-fill-1",
            "id": "remember",
        })


class UserSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)

        self.fields["email"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""


class UserResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserResetPasswordForm, self).__init__(*args, **kwargs)


# TODO hide label for password reset
# TODO add contact us form for password reset view


# Stuff from cookiecutter

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'company_name',
                  'address', 'city', 'region', 'country', 'postal_code')
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'company_name': forms.TextInput(attrs={"class": "form-control"}),
            'address': forms.TextInput(attrs={"class": "form-control"}),
            'city': forms.TextInput(attrs={"class": "form-control"}),
            'region': forms.TextInput(attrs={"class": "form-control"}),
            'country': forms.TextInput(attrs={"class": "form-control"}),
            'postal_code': forms.TextInput(attrs={"class": "form-control"}),
        }


class UserCreationForm(admin_forms.UserCreationForm):
    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
