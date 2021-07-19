from django import forms

from .models import Invoice
from customers.models import Customer

CHOICES_VALID = [
    ('True', 'Yes'),
    ('False', 'No')
]

CHOICES_STATUS = [
    ('UNPAID', 'Unpaid'),
    ('PAID', 'Paid')
]

CHOICES_TAX_RATE = [
    ('0.05', '5%'),
    ('0.10', '10%')
]

CHOICES_DISCOUNT_RATE = [
    ('0.05', '5%'),
    ('0.10', '10%')
]


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice

        fields = ('customer', 'valid', 'expiration_date', 'status', 'tax_rate',
                  'discount')
        widgets = {
            'expiration_date': forms.DateInput(format=('%Y-%m-%d'),
                                               attrs={"class": "form-control",
                                                      "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(InvoiceForm, self).__init__(*args, **kwargs)

        self.created_by = kwargs['initial']['created_by']

        self.fields['customer'] = forms.ModelChoiceField(
            queryset=Customer.objects.filter(created_by=self.request.user),
            widget=forms.Select(attrs={"class": "form-control"})
        )
        self.fields['valid'] = forms.ChoiceField(choices=CHOICES_VALID,
                                                 widget=forms.Select(
                                                     attrs={"class": "form-control"}))
        self.fields['status'] = forms.ChoiceField(choices=CHOICES_STATUS,
                                                  widget=forms.Select(
                                                      attrs={"class": "form-control"}))
        self.fields['tax_rate'] = forms.ChoiceField(choices=CHOICES_TAX_RATE,
                                                    widget=forms.Select(
                                                        attrs={"class": "form-control"}))
        self.fields['discount'] = forms.ChoiceField(choices=CHOICES_DISCOUNT_RATE,
                                                    widget=forms.Select(
                                                        attrs={"class": "form-control"}))

    def save(self, commit=True):
        obj = super(InvoiceForm, self).save(False)
        obj.created_by = self.created_by
        commit and obj.save()
        return obj
