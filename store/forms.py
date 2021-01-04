from django import forms

from django_countries.widgets import CountrySelectWidget

from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ('address', 'city', 'province', 'country', 'zipcode')
        widgets = {'country': CountrySelectWidget(
            layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0;width: 20px; height: 20px;" src="{country.flag}">'
        )}