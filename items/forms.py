from django import forms
from django.forms import inlineformset_factory

from .models import Item
from invoices.models import Invoice


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = ('name', 'description', 'cost', 'quantity')
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.TextInput(attrs={"class": "form-control"}),
            'cost': forms.NumberInput(attrs={"class": "form-control"}),
            'quantity': forms.NumberInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, user=None, **kwargs):
        if user:
            self.user = user
        super(ItemForm, self).__init__(*args, **kwargs)
        # self.fields['name'] = forms.ModelChoiceField(queryset=Item.objects.filter(created_by=self.user),
        #                                          widget=forms.Select(
        #                                              attrs={"class": "form-control"}))

    def save(self, commit=True):
        obj = super(ItemForm, self).save(False)
        obj.created_by = self.user
        commit and obj.save()
        return obj

ItemFormset = inlineformset_factory(Invoice, Item,
                                    form=ItemForm,
                                    extra=1)
