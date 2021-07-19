from django.urls import include, path, re_path

from .views import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerDetailView,
    CustomerListView,
    CustomerUpdateView,
)

app_name = 'customers'

urlpatterns = [
    path('list', CustomerListView.as_view(), name='customer_list'),
    path('<uuid:slug>', CustomerDetailView.as_view(), name='customer_detail'),
    path('create', CustomerCreateView.as_view(), name='customer_create'),
    path('update/<uuid:slug>', CustomerUpdateView.as_view(), name='customer_update'),
    path('delete/<uuid:slug>', CustomerDeleteView.as_view(), name='customer_delete'),
]
