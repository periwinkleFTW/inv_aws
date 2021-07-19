from django.contrib import admin

from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'cost', 'created_by']
    readonly_fields = ['id', 'created_on']


admin.site.register(Item, ItemAdmin)
