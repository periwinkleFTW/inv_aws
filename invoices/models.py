import uuid
from decimal import Decimal

from django.db import models
from django.urls import reverse

from customers.models import Customer
from invoice_app.users.models import User




class Invoice(models.Model):
    slug = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='invoices',
    )
    valid = models.BooleanField(default=True)
    expiration_date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=20)

    tax_rate = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    discount = models.DecimalField(decimal_places=2, max_digits=3, default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('invoices:invoice_detail', args=[str(self.slug)])

#TODO calculations are wrong with inline formsets

    def total_items_cost(self):
        total = 0
        items = self.items.all()

        for item in items:
            total += item.cost * item.quantity
        return total

    def discounted_amt(self):
        discount_amount = 0
        discount_amount = self.total_items_cost() * self.discount
        discount_amount = round(discount_amount, 2)
        return discount_amount


    def taxes(self):
        result = self.total_items_cost() * self.tax_rate
        result = round(result, 2)
        return result

    def total(self):
        return self.total_items_cost() + self.taxes() + self.discounted_amt()

    def paid(self):
        return self.status == 'Paid'

    def unpaid(self):
        return self.status == 'Unpaid'

    def draft(self):
        return self.status == 'Draft'
