from django.urls import path

from .views import (
    InvoiceCreateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    InvoiceListView,
    InvoiceUpdateView,
)

app_name = 'invoices'

urlpatterns = [
    path('list', InvoiceListView.as_view(), name='invoice_list'),
    path('<uuid:slug>', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('create', InvoiceCreateView.as_view(), name='invoice_create'),
    path('update/<uuid:slug>', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('delete/<uuid:slug>', InvoiceDeleteView.as_view(), name='invoice_delete'),
]
