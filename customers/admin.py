from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'city', 'created_by']


admin.site.register(Customer, CustomerAdmin)
