from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Customer
from .forms import CustomerForm
from invoices.models import Invoice


class CustomerTests(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )
        self.customer1 = Customer.objects.create(
            name='Harry Potter',
            phone='111-323-4424',
            email='flaccidwand@hogwarts.com',
            company_name='ChocFrog Inc',
            address='346 Diagon Alley',
            city='London',
            region='Worcestershire',
            country='England',
            postal_code='424234324',
            created_by=self.user1
        )
        self.invoice1 = Invoice.objects.create(
            customer=self.customer1,
            valid=True,
            expiration_date=datetime.now(),
            status='Unpaid',
            tax_rate=12,
            discount=1,
            created_by=self.user1
        )

        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='testuser2@email.com',
            password='testpass123'
        )
        self.customer2 = Customer.objects.create(
            name='Frodo Baggins',
            phone='6666666',
            email='gayforsam@hogwarts.com',
            company_name='Rim that Ring',
            address='45 Grassy Path',
            city='Shire',
            region='Hobbiton',
            country='Middle Earth',
            postal_code='T6G8H6',
            created_by=self.user2
        )
        self.invoice2 = Invoice.objects.create(
            customer=self.customer2,
            valid=True,
            expiration_date=datetime.now(),
            status='Paid',
            tax_rate=0,
            discount=30,
            created_by=self.user2
        )

    def test_customer_listing(self):
        self.assertEqual(f'{self.customer1.name}', 'Harry Potter')
        self.assertEqual(f'{self.customer1.phone}', '111-323-4424')
        self.assertEqual(f'{self.customer1.email}', 'flaccidwand@hogwarts.com')
        self.assertEqual(f'{self.customer1.company_name}', 'ChocFrog Inc')
        self.assertEqual(f'{self.customer1.address}', '346 Diagon Alley')
        self.assertEqual(f'{self.customer1.city}', 'London')
        self.assertEqual(f'{self.customer1.region}', 'Worcestershire')
        self.assertEqual(f'{self.customer1.country}', 'England')
        self.assertEqual(f'{self.customer1.postal_code}', '424234324')

        self.assertEqual(f'{self.customer2.name}', 'Frodo Baggins')
        self.assertEqual(f'{self.customer2.phone}', '6666666')
        self.assertEqual(f'{self.customer2.email}', 'gayforsam@hogwarts.com')
        self.assertEqual(f'{self.customer2.company_name}', 'Rim that Ring')
        self.assertEqual(f'{self.customer2.address}', '45 Grassy Path')
        self.assertEqual(f'{self.customer2.city}', 'Shire')
        self.assertEqual(f'{self.customer2.region}', 'Hobbiton')
        self.assertEqual(f'{self.customer2.country}', 'Middle Earth')
        self.assertEqual(f'{self.customer2.postal_code}', 'T6G8H6')

    def test_customer_list_view_for_logged_in_user(self):
        self.client.login(email='testuser1@email.com', password='testpass123')
        response = self.client.get(reverse('customers:customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertNotContains(response, 'Frodo Baggins')
        self.assertTemplateUsed(response, 'customers/customer-table.html')

        self.client.login(email='testuser2@email.com', password='testpass123')
        response = self.client.get(reverse('customers:customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Frodo Baggins')
        self.assertNotContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'customers/customer-table.html')

    def test_customer_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('customers:customer_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/customers/list' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/customers/list' % (reverse('account_login')))
        self.assertContains(response, 'Login')

    def test_customer_detail_view(self):
        self.client.login(email='testuser1@email.com', password='testpass123')
        response = self.client.get(self.customer1.get_absolute_url())
        no_response = self.client.get('/customers/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, '111-323-4424')
        self.assertContains(response, 'flaccidwand@hogwarts.com')
        self.assertContains(response, 'ChocFrog Inc')
        self.assertContains(response, '346 Diagon Alley')
        self.assertContains(response, 'London')
        self.assertContains(response, 'Worcestershire')
        self.assertContains(response, 'England')
        self.assertContains(response, '424234324')
        self.assertTemplateUsed(response, 'customers/customer-detail.html')
        self.client.logout()

        self.client.login(email='testuser2@email.com', password='testpass123')
        response = self.client.get(self.customer2.get_absolute_url())
        no_response = self.client.get('/customers/98765/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Frodo Baggins')
        self.assertContains(response, '6666666')
        self.assertContains(response, 'gayforsam@hogwarts.com')
        self.assertContains(response, 'Rim that Ring')
        self.assertContains(response, '45 Grassy Path')
        self.assertContains(response, 'Shire')
        self.assertContains(response, 'Hobbiton')
        self.assertContains(response, 'Middle Earth')
        self.assertContains(response, 'T6G8H6')
        self.assertTemplateUsed(response, 'customers/customer-detail.html')
        self.client.logout()

    def test_customer_detail_view_invoices_for_this_customer(self):
        self.client.login(email='testuser1@email.com', password='testpass123')
        response = self.client.get(self.customer1.get_absolute_url())
        self.assertEqual(f'{self.invoice1.customer.name}', 'Harry Potter')
        self.assertEqual(f'{self.invoice1.status}', 'Unpaid')
        self.client.logout()

        self.client.login(email='testuser2@email.com', password='testpass123')
        response = self.client.get(self.customer2.get_absolute_url())
        self.assertEqual(f'{self.invoice2.customer.name}', 'Frodo Baggins')
        self.assertEqual(f'{self.invoice2.status}', 'Paid')
        self.client.logout()

    def test_customer_delete_view(self):
        self.client.login(email='testuser1@email.com', password='testpass123')
        response = self.client.post(reverse('customers:customer_delete',
                                            kwargs={'pk': self.customer1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Customer.objects.filter(pk=self.customer1.id).exists())


