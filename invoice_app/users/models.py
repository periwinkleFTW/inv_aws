import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Invoices Project."""

    #: First and last name do not cover name patterns around the globe
    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False,
    # )
    first_name = models.CharField(_("First name"), max_length=80)
    last_name = models.CharField(_("Last name"), max_length=80)
    username = models.CharField(_("Username"), unique=True, max_length=80)
    email = models.EmailField(_("Email"), unique=True, max_length=100)
    phone = models.CharField(_("Phone"), blank=True, max_length=50)
    company_name = models.CharField(_("Company name"), blank=True, max_length=100)
    address = models.CharField(_("Address"), blank=True, max_length=100)
    city = models.CharField(_("City"), blank=True, max_length=100)
    region = models.CharField(_("Region"), blank=True, max_length=100)
    country = models.CharField(_("Country"), blank=True, max_length=100)
    postal_code = models.CharField(_("Postal Code"), blank=True, max_length=100)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    active = models.BooleanField(_("Active"), default=True)
    staff = models.BooleanField(_("Staff"), default=False)


    class Meta:
        ordering = ['email']

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        # return reverse("users:detail", kwargs={"username": self.username})
        return reverse("invoices:invoice_list")
