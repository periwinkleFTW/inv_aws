import uuid

from django.db import models
from django.urls import reverse

from invoice_app.users.models import User

REGION_CHOICES = [
    ('Alberta', 'AB'),
    ('British Columbia', 'BC'),
    ('Manitoba', 'MB'),
    ('New Brunswick', 'NB'),
    ('Newfoundland and Labrador', 'NL'),
    ('Nova Scotia', 'NS'),
    ('Ontario', 'ON'),
    ('Prince Edward Island', 'PE'),
    ('Quebec', 'QC'),
    ('Saskatchewan', 'SK'),
    ('Northwest Territories', 'NWT'),
    ('Nunavut', 'NT'),
    ('Yukon', 'YT'),

]


class Customer(models.Model):
    slug = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=50, null=False, blank=True)
    email = models.EmailField(null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)

    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True, choices=REGION_CHOICES)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customers:customer_detail', args=[str(self.slug)])

    def invoices(self):
        """
        Returns all invoices for this customer
        """
        return Invoice.objects.filter(customer=self).count()
