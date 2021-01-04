import random

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse

from accounts.models import User
from accounts.utils import generate_token

from django_countries.fields import CountryField
# Create your models here.

class Image(models.Model):
    image = models.ImageField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return "image for " + self.product.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    shipping_cost = models.FloatField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.name

    def short_name(self):
        return self.name[:15] + "..." if len(self.name)>15 else self.name

    def short_description(self):
        return self.description[:30] + '...'

class Cart(models.Model):
    products = models.ManyToManyField(Product, 'cart')
    order = models.OneToOneField('Order', null=True, on_delete=models.SET_NULL)

    def cart_total(self):
        total = 0
        products = self.products.all()
        for p in products:
            total += p.price
        return round(total,2)

    def __str__(self):
        if self.order:
            return 'Cart - Order: ' + self.order.order_id
        return 'Cart' + str(self.id)

class ShippingAddress(models.Model):
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = CountryField(blank_label='(select country)')
    zipcode = models.IntegerField()
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.address + " " + self.city + ", " + self.province + " " + str(self.zipcode)  + ", " + str(self.country )


class OrderManager(models.Manager):

    def get_order_from_session(self, request):
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        order = cart.order

        return order

class Order(models.Model):
    CHOICES = (
        ('Processing', 'processing'),
        ('Paid', 'paid'),
        ('Shipping', 'shipping'),
        ('Closed', 'closed')
    )
    order_id = models.SlugField(blank=True, unique=True)
    total = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, related_name='order', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=CHOICES, default='Processing')
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.order_id

    @property
    def subtotal(self):
        order_subtotal = 0
        try:
            for p in self.cart.products.all():
                order_subtotal += p.price
        except:
            pass
        return round(order_subtotal, 2)

    def get_total(self):
        total = 0
        if self.cart:
            for p in self.cart.products.all():
                total += p.price + p.shipping_cost
            return round(total, 2)
        return round(total, 2)

    def get_order_link(self):
        link = reverse('accounts:order-details', kwargs={'order_id':self.order_id})
        return link

@receiver(pre_save, sender=Order)
def pre_save_order(instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = generate_token(8)

    instance.total = instance.subtotal + 10.99
