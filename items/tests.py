from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Item


class ItemTests(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )
        self.item1 = Item.objects.create(
            name='Cucumber',
            description='Green and cool',
            cost=3,
            quantity=12,
            created_by=self.user1
        )
        # self.invoice1 = Invoice.objects.create(
        #     customer=self.customer1,
        #     valid=True,
        #     expiration_date=datetime.now(),
        #     status='Unpaid',
        #     tax_rate=12,
        #     discount=1,
        #     created_by=self.user1
        # )

        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='testuser2@email.com',
            password='testpass123'
        )
        self.item2 = Item.objects.create(
            name='Apple',
            description='Red and sweet',
            cost=1,
            quantity=25,
            created_by=self.user2
        )
        # self.invoice2 = Invoice.objects.create(
        #     customer=self.customer2,
        #     valid=True,
        #     expiration_date=datetime.now(),
        #     status='Paid',
        #     tax_rate=0,
        #     discount=30,
        #     created_by=self.user2
        # )

    def test_item_listing(self):
        self.assertEqual(f'{self.item1.name}', 'Cucumber')
        self.assertEqual(f'{self.item1.description}', 'Green and cool')
        self.assertEqual(f'{self.item1.cost}', '3')
        self.assertEqual(f'{self.item1.quantity}', '12')

        self.assertEqual(f'{self.item2.name}', 'Apple')
        self.assertEqual(f'{self.item2.description}', 'Red and sweet')
        self.assertEqual(f'{self.item2.cost}', '1')
        self.assertEqual(f'{self.item2.quantity}', '25')

    def test_item_list_view_for_logged_in_user(self):
        self.client.login(email='testuser1@email.com', password='testpass123')
        response = self.client.get(reverse('items:item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cucumber')
        self.assertNotContains(response, 'Apple')
        self.assertTemplateUsed(response, 'items/item-table.html')

        self.client.login(email='testuser2@email.com', password='testpass123')
        response = self.client.get(reverse('items:item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple')
        self.assertNotContains(response, 'Cucumber')
        self.assertTemplateUsed(response, 'items/item-table.html')

    def test_item_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('items:item_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/items/list' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/items/list' % (reverse('account_login')))
        self.assertContains(response, 'Login')

    def test_item_detail_view(self):
        self.client.login(email='testuser1@email.com', password='testpass123')
        response = self.client.get(self.item1.get_absolute_url())
        no_response = self.client.get('/items/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Cucumber')
        self.assertContains(response, 'Green and cool')
        self.assertContains(response, '3')
        self.assertContains(response, '12')
        self.assertTemplateUsed(response, 'items/item-detail.html')
        self.client.logout()

        self.client.login(email='testuser2@email.com', password='testpass123')
        response = self.client.get(self.item2.get_absolute_url())
        no_response = self.client.get('/items/98765/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Red and sweet')
        self.assertContains(response, '1')
        self.assertContains(response, '25')
        self.assertTemplateUsed(response, 'items/item-detail.html')
        self.client.logout()



