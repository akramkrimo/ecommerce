from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('order-details/<slug:order_id>', views.OrderDetails.as_view(), name='order-details'),
    path('change-email/', views.change_email, name='change-email'),
    path('token-sent-succes/', views.token_sent_success, name='token_sent_success'),
    path('token-validation/<str:token>', views.old_token_validation, name='old-token-validation'),
    path('new-email-token', views.new_email_token, name='new-email-token'),
    path('new-token-validation/<str:token>', views.new_token_validation, name='new-token-validation'),
    path('new-email-token-sent-success', views.new_email_token_sent_success, name='new-email-token-sent-success'),
    path('new-token-validated', views.new_token_validated, name='new-token-validated'),
    path('add-shipping-address', views.add_shipping_address, name='add-shipping-address'),
    path('delete-address/<int:address_pk>', views.delete_shipping_address, name='delete-address'),
]