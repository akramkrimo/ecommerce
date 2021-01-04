from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_view, name='payment'),
    path('charge-existing-card/<int:card_id>', views.charge_existing_card, name='charge-existing-card'),
    path('success', views.payment_success, name='payment-success'),
    path('save-card', views.save_card, name='save-card'),
    path('delete-card/<int:card_id>', views.delete_card, name='delete-card')
]