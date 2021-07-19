from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ItemForm
from .models import Item


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    context_object_name = 'item_list'
    template_name = 'items/item-table.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'items/item-detail.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    context_object_name = 'item_create'
    template_name = 'items/item-create.html'
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.save()
        return super().form_valid(form)

    # Pass the request to the form to allow filtering by user id
    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs.update({
                       'user': self.request.user})
        return kwargs

    # Added this because form was not saving user id
    def get_initial(self):
        self.initial.update({'created_by': self.request.user})
        return self.initial


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    context_object_name = 'item_update'
    template_name = 'items/item-update.html'
    login_url = 'account_login'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    # Pass the request to the form to allow filtering by user id
    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'items/item-delete.html'
    login_url = 'account_login'

    success_url = reverse_lazy('items:item_list')
