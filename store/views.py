from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.urls import reverse

from .documents import ProductDocument
from .forms import ShippingAddressForm
from .models import Product, Cart, Order, ShippingAddress

import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET


def main_page(request):
    q = request.GET.get('q')
    if q:
        s = ProductDocument.search().query("multi_match", query=q, fields=['name', 'description'])
        products = s.to_queryset()
    else:
        products = Product.objects.all()
    
    cart_id = request.session.get('cart_id')
    cart = None
    if cart_id:
        cart = Cart.objects.get(id=cart_id)

    context = {
        'products': products,
        'cart': cart
    }
    return render(request, 'store/home.html', context)

class ProductDetails(DetailView):
    queryset = Product.objects.all()
    template_name = 'store/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        
        # this should be added to the cart manager because it's getting repetetive
        cart_id = self.request.session.get('cart_id')
    
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            self.request.session['cart_id'] = cart.pk
    
        context['cart'] = cart
        return context


def add_remove_from_cart(request, product_id):
    # get the cart id from the session storage if it exists

    redirect_url = request.POST.get('redirect_url')

    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
    # if we don't have any cart id stored in the session, we add one
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    
    # get the product using the id provided in the url
    product = Product.objects.get(id=product_id)

    # add or remove product
    if product in cart.products.all():
        cart.products.remove(product)
    else:
        cart.products.add(product)

    return redirect(redirect_url)

def cart_view(request):
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.pk

    return render(request, 'store/cart.html', {'cart':cart})

# you can add the id of an existing shipping address as an argument and use the same view
# without the nedd to create another view for existing shipping addresses,
# give that argument the value of None
def shipping_address_info(request):

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format(
            reverse('accounts:login'),
            request.path
        ))
    
    form = ShippingAddressForm(request.POST or None)
    cart_id = request.session['cart_id']
    cart = Cart.objects.get(id=cart_id)
    order = None

    # if the user is going to use an existing shipping address
    shipping_address_id = request.POST.get('existing_address')

    if shipping_address_id:
        shipping_address = ShippingAddress.objects.get(id=shipping_address_id)
        order = Order.objects.create(
            shipping_address = shipping_address,
            user = request.user
        )
        cart.order = order
        cart.save()
        return redirect('payments:payment')
    
    # if the user decides to use a new shipping address
    if form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        order = Order.objects.create(
            shipping_address = address,
            user = request.user
        )
        cart.order = order
        cart.save()
        return redirect('payments:payment')

    context = {
        'form': form,
        'order': order
    }
    return render(request, 'payments/checkout.html', {'form':form})


