from django.contrib import admin

from items.models import Item

from .models import Invoice


class ItemInline(admin.TabularInline):
    model = Item


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]
    list_display = ['id', 'status', 'customer', 'created_on', 'expiration_date', 'created_by',]


admin.site.register(Invoice, InvoiceAdmin)
