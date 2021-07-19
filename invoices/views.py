from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import InvoiceForm
from .models import Invoice
from items.forms import ItemFormset


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    context_object_name = 'invoice_list'
    template_name = 'invoices/invoice-table.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    context_object_name = 'invoice'
    template_name = 'invoices/invoice-detail.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice-create.html'
    login_url = 'account_login'

    # Pass the request to the form to allow filtering by user id
    def get_form_kwargs(self):
        kwargs = super(InvoiceCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    # Added this because form was not saving user id
    def get_initial(self):
        self.initial.update({'created_by': self.request.user})
        return self.initial

    def get_success_url(self):
        return reverse_lazy('invoices:invoice_detail', kwargs={'slug': self.object.slug})

    # Inline formsets from medium post https://medium.com/@adandan01/django-inline-formsets-example-mybook-420cc4b6225d
    def get_context_data(self, **kwargs):
        data = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = ItemFormset(self.request.POST,
                                        instance=self.object,
                                        form_kwargs={'user': self.request.user})
        else:
            data['items'] = ItemFormset(instance=self.object,
                                        form_kwargs={'user': self.request.user})
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            self.object = form.save()

            if items.is_valid():
                items.instance = self.object
                items.save()
        return super(InvoiceCreateView, self).form_valid(form)
    # End medium post stuff


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    context_object_name = 'invoice_update'
    template_name = 'invoices/invoice-update.html'
    login_url = 'account_login'

    # Pass the request to the form to allow filtering by user id
    def get_form_kwargs(self):
        kwargs = super(InvoiceUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    # Added this because form was not saving user id
    def get_initial(self):
        self.initial.update({'created_by': self.request.user})
        return self.initial

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


    def get_context_data(self, **kwargs):
        data = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = ItemFormset(self.request.POST, instance=self.object,
                                        form_kwargs={'user': self.request.user})
        else:
            data['items'] = ItemFormset(instance=self.object,
                                        form_kwargs={'user': self.request.user})
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            self.object = form.save()

            if items.is_valid():
                items.instance = self.object
                items.save()
        return super(InvoiceUpdateView, self).form_valid(form)




class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'invoices/invoice-delete.html'
    login_url = 'account_login'

    success_url = reverse_lazy('invoices:invoice_list')
