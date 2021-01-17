from django.urls import resolve, reverse
from django.test import TestCase

from store import views

class TestUrls(TestCase):

    def test_home_page(self):
        url = reverse('store:home-page')
        view = resolve(url).func

        self.assertEquals(view, views.main_page)

    def test_product_details(self):
        url = reverse('store:product-details', args=['1'])
        view = resolve(url).func

        self.assertEquals(view.view_class, views.ProductDetails)

    def test_cart_view(self):
        url = reverse('store:cart')
        view = resolve(url).func

        self.assertEquals(view, views.cart_view)


    def test_add_remove_from_cart(self):
        url = reverse('store:add-remove-from-cart')
        view = resolve(url).func

        self.assertEquals(view, views.add_remove_from_cart)

    def test_shipping_address_info(self):
        url = reverse('store:shipping-address')
        view = resolve(url).func

        self.assertEquals(view, views.shipping_address_info)
