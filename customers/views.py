from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from invoices.models import Invoice

from .forms import CustomerForm
from .models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customer_list'
    ordering = ['-created_on']
    template_name = 'customers/customer-table.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customers/customer-detail.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        # filter by user id
        context['invoice_list'] = Invoice.objects.filter(created_by=self.request.user)
        # filter by customer
        context['invoice_list'] = Invoice.objects.filter(customer=self.object.id)
        return context


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    context_object_name = 'customer_create'
    template_name = 'customers/customer-create.html'
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.save()
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    context_object_name = 'customer_update'
    template_name = 'customers/customer-update.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customers/customer-delete.html'
    login_url = 'account_login'

    success_url = reverse_lazy('customers:customer_list')
