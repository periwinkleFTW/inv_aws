from django.urls import path

from .views import (
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
)

app_name = 'items'

urlpatterns = [
    path('list', ItemListView.as_view(), name='item_list'),
    path('<uuid:slug>', ItemDetailView.as_view(), name='item_detail'),
    path('create', ItemCreateView.as_view(), name='item_create'),
    path('update/<uuid:slug>', ItemUpdateView.as_view(), name='item_update'),
    path('delete/<uuid:slug>', ItemDeleteView.as_view(), name='item_delete'),
]
