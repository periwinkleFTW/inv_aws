from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = ('name', 'phone', 'email', 'address',
                  'city', 'region', 'postal_code', 'country')
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'address': forms.TextInput(attrs={"class": "form-control"}),
            'city': forms.TextInput(attrs={"class": "form-control"}),
            'region': forms.TextInput(attrs={"class": "form-control"}),
            'country': forms.TextInput(attrs={"class": "form-control"}),
            'postal_code': forms.TextInput(attrs={"class": "form-control"}),
        }
