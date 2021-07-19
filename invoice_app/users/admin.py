from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from invoice_app.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "first_name", "is_superuser", "id"]
    search_fields = ["username"]
