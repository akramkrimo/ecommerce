from django.test import SimpleTestCase

from store.forms import ShippingAddressForm

class ShippingAddressFormTest(SimpleTestCase):

    def test_form_valid(self):
        form = ShippingAddressForm(data={
            'address': 'some address',
            'province': 'some province',
            'city': 'some city',
            'country': 'DZ',
            'zipcode': 11111,
        })

        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # empty form is invalid
        form = ShippingAddressForm()
        self.assertFalse(form.is_valid())

        # if one field is empty, the form is invalid
        form = ShippingAddressForm(data={
            'address': '',
            'province': 'some province',
            'city': 'some city',
            'country': 'DZ',
            'zipcode': 11111,
        })
        self.assertFalse(form.is_valid())

        # wrong types of field result in an invalid form

        # integers should not be anything else
        form = ShippingAddressForm(data={
            'address': 'some address',
            'province': 'some province',
            'city': 'some city',
            'country': 'DZ',
            'zipcode': 'zip code',
        })
        self.assertFalse(form.is_valid())

        # strings should not be anything else
        form = ShippingAddressForm(data={
            'address': 'some address',
            'province': 'some province',
            'city': 'some city',
            'country': True,
            'zipcode': 'zip code',
        })
        self.assertFalse(form.is_valid())