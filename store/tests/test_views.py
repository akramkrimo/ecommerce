from django.contrib.auth.models import AnonymousUser
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from accounts.models import User
from store.models import Product, Cart, ShippingAddress


class TestViews(TestCase):
    fixtures = ['store.json', 'users.json']

    def setUp(self):
        # get a product to test views with products
        self.product = Product.objects.first()

        # calling this view will store a cart_id in the session
        self.client.get('/cart/')

        # get a user so that you can access user-authenticated-only views
        self.user = User.objects.first()
        self.client.force_login(self.user)

    def test_GET_home_page(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response=response, template_name='store/home.html')
        self.assertEqual(response.status_code, 200)

    def test_GET_product_details(self):
        pk = self.product.pk
        response = self.client.get(f'/products/{pk}')

        # make sure the view is working properly
        # using the right template
        # providing the right contet

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='store/product_details.html')
        self.assertEqual(response.context['object'], self.product)

        # make sure if the product does not exist, an error is raised
        response = self.client.get(f'/products/123456789')
        self.assertEqual(response.status_code, 404)

    def test_cart_view(self):
        response = self.client.get('/cart/')
        session = self.client.session

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')
        self.assertIsNotNone(response.context['cart'])
        self.assertIsNotNone(session['cart_id'])
    
    def test_GET_add_remove_from_cart(self):
        response = self.client.get(f'/cart/add-or-remove-from-cart')

        self.assertEqual(response.status_code, 405)

    def test_POST_add_remove_from_cart(self):

        # if the product id does not exist, raise an error
        response = self.client.post({'product_id': 0, 'redirect_url': '/'})

        self.assertEqual(response.status_code, 404)

        # make sure the cart is empty
        cart = Cart.objects.get(
            pk=self.client.session['cart_id']
        )
        self.assertEqual(cart.products.count(), 0)

        # if the product id is valid, make sure the product was added to the cart
        response = self.client.post('/cart/add-or-remove-from-cart', {'product_id': self.product.pk, 'redirect_url': '/'})

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.product, cart.products.all())

        # if the product id is valid and the product is already in the cart
        # make sure it is removed
        response = self.client.post(f'/cart/add-or-remove-from-cart', {'product_id': self.product.pk, 'redirect_url': '/'})

        self.assertNotIn(self.product, cart.products.all())
        self.assertEqual(response.status_code, 302)


    def test_GET_shipping_address_info_not_authenticated(self):
        self.client.logout()
        response = self.client.get('/shipping-address/')

        redirect_url = reverse('accounts:login') + '?next=/shipping-address/'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_GET_shipping_address_info_authenticated(self):
        response = self.client.get('/shipping-address/')

        self.assertEqual(str(response.context['user']), 'd.akram13@gmail.com')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('payments/checkout.html')
        self.assertIsNotNone(response.context['form'])

    def test_POST_existing_shipping_address(self):
        response = self.client.post('/shipping-address/', {'existing_address': 1})

        self.assertEqual(response.status_code, 302)

    def test_POST_non_existing_address(self):
        self.user

        # make sure the user has only one address
        self.assertEqual(self.user.addresses.count(), 1)

        data = {
            'address': 'some address',
            'province': 'some province',
            'city': 'some city',
            'country': 'DZ', # this is an option list, so they can't mess it up
            'zipcode': 11111,
        }
        response = self.client.post('/shipping-address/', data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payments:payment'))

        # the user had initially one address, and by adding a new one
        # they should have two now

        self.assertEqual(self.user.addresses.count(), 2)

    def test_POST_invalid_non_existing_address(self):

        data = {
            'address': 'some address',
            'province': 'some province',
            'city': 'some city',
            'country': 'DZ', # this is an option list, so they can't mess it up
            'zipcode': 'abcde', # form will be invalid because zipcode must be integer not str
        }
        response = self.client.post('/shipping-address/', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/checkout.html')

        # make sure no order was created, orders are only created when a valid address is provided

        self.assertIsNone(response.context['order'])
        self.assertFormError(response, 'form', 'zipcode', 'Enter a whole number.')
