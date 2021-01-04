from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView

import json

from .models import Card

from store.models import Cart, Order

# Stripe
import stripe

stripe.api_key = settings.STRIPE_SECRET

# Create your views here.


def payment_view(request):
    order = Order.objects.get_order_from_session(request)

    if order.status != 'Processing':
        return redirect('store:payment-success')
 
    if request.method == 'POST':
        try:
            total = int(order.get_total() * 100)
            intent = stripe.PaymentIntent.create(
                amount = total,
                currency = 'usd',
                customer = request.user.customer_id,
                receipt_email = request.user.email,
            )
            return JsonResponse({
            'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


    return render(request, 'payments/checkout.html', {'order':order})

@require_POST
def charge_existing_card(request, card_id):
    order = Order.objects.get_order_from_session(request)

    card = Card.objects.get(id=card_id)

    intent = stripe.PaymentIntent.create(
        amount = int(order.get_total() * 100),
        currency = 'usd',
        customer = card.user.customer_id,
        payment_method = card.payment_method,
        off_session=True,
        confirm=True,
    )
    return redirect('payments:payment-success')

@require_POST
def save_card(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
        payment_method_id = post_data['payment_method']
        pm = stripe.PaymentMethod.retrieve(id=payment_method_id)
        new_card = pm['card']
        user_cards = request.user.cards.all()
        if not user_cards.filter(fingerprint=new_card['fingerprint']):
            card = Card.objects.create(
                brand = pm['card']['brand'],
                last_4 = pm['card']['last4'],
                fingerprint = pm['card']['fingerprint'],
                payment_method = pm['id'],
                user = request.user
            )
            stripe.Customer.modify(
                card.user.customer_id,
                invoice_settings={'default_payment_method': payment_method_id}
            )
            return JsonResponse({
                'message': 'Card has been successfully saved'
            })

        else:
            return JsonResponse({
                'error_message': 'Card already exists'
            })

    except Exception as e:
        return JsonResponse({'error': str(e)})

# deleting a card should also send a request to stripe to detatch the card from the customer
def delete_card(request, card_id):
    card = Card.objects.get(id=card_id)
    stripe.PaymentMethod.detach(
        card.payment_method
    )
    card.delete()
    return redirect('accounts:settings')


def payment_success(request):
    order = Order.objects.get_order_from_session(request)

    if order.status == 'Processing':
        order.status = 'Paid'
        order.save()
        del request.session['cart_id']

    return render(request, 'payments/checkout.html', {'order': order})