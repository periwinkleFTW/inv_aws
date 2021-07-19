import uuid

from django.db import models
from django.urls import reverse

from invoices.models import Invoice
from invoice_app.users.models import User


class Item(models.Model):
    slug = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items:item_detail', args=[str(self.slug)])

    def total(self):
        return self.cost * self.quantity
