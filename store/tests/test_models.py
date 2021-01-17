from django.test import TestCase

from accounts.models import User
from store.models import Product, Cart, Order, ShippingAddress

class ProductModelTest(TestCase):
    fixtures = ['store.json', 'users.json']

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.first()

    def test_shipping_cost_label(self):

        shipping_cost_name = self.product._meta.get_field('shipping_cost').verbose_name

        self.assertEqual(shipping_cost_name, 'shipping cost')

    def test__str__(self):
        name = self.product.name

        self.assertIs(str(self.product), name)

    def test_short_name(self):

        #  the product's name is longer than 15 + 3 (3 for the 3 dots '...')
        product_name = self.product.name

        if len(product_name) > 15:
            self.assertTrue(len(self.product.short_name()) < len(product_name))
            self.assertEqual(len(self.product.short_name()), 18)
        else:
            self.assertEqual(self.product.short_name(), self.product.name)

    def test_short_description(self):

        # the product's description is longer than 30 + 3 (again 3 for the 3 dots '...')
        product_description = self.product.description

        if len(product_description) > 30:
            self.assertEqual(self.product.short_description(), product_description[:30] + '...' )
            self.assertEqual(len(self.product.short_description()), 33)
        else:
            self.assertEqual(self.product.short_description(), product_description + '...' )
            self.assertEqual(len(self.product.short_description()), len(self.product.description) + 3)

class CartModelTest(TestCase):
    fixtures = ['store.json', 'users.json']

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.first()
        cls.cart = Cart.objects.create()
        cls.cart.products.add(cls.product)


    def test_cart_has_product(self):
        # no cart should be created in the views unless products are added to it
        products_count = self.cart.products.count()
        self.assertNotEqual(products_count, 0)

    def test__str__with_no_order_object(self):
        cart_string = 'Cart' + str(self.cart.id)
        
        self.assertEqual(str(self.cart), cart_string)

    def test_cart_total(self):
        # calculate the sum of the products' prices, and round it up
        total = round( sum([p.price for p in self.cart.products.all()]), 2)
        
        self.assertEqual(self.cart.cart_total(), total)

class OrderModelTest(TestCase):
    fixtures = ['store.json', 'users.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.first()
        cls.address = ShippingAddress.objects.create(
            address = 'address1',
            city = 'city1',
            province = 'province1',
            country = 'DZ',
            zipcode = 10000,
            user = cls.user
        )
        cls.order = Order.objects.create(
            shipping_address = cls.address,
            user = cls.user
        )   # the rest of the fields have default values, we dont have to fill them up manually

    def test_order__str__(self):
        self.assertEqual(str(self.order), self.order.order_id)

    def test_order_pre_save_signal(self):
        self.assertIsNotNone(self.order.order_id)

    def test_subtotal_with_no_cart(self):
        self.assertEqual(self.order.subtotal, 0)

    def test_get_total_with_no_cart(self):
        self.assertEqual(self.order.get_total(), 0)

    def test_get_order_link(self):
        link = f'/accounts/order-details/{self.order.order_id}'
        self.assertEqual(self.order.get_order_link(), link)

    def test_subtotal_with_cart(self):
        cart = Cart.objects.create()
        cart.products.add(Product.objects.first())
        cart.order = self.order
        
        subtotal = cart.cart_total()
        
        self.assertEqual(self.order.subtotal, subtotal)

    def test_get_total_no_cart(self):
        cart = Cart.objects.create()
        cart.products.add(Product.objects.first())
        cart.order = self.order

        order_total = round( sum( [p.price + p.shipping_cost for p in cart.products.all()] ), 2)
        
        self.assertEqual(self.order.get_total(), order_total)