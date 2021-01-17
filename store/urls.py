from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main_page, name='home-page'),
    path('products/<int:pk>', views.ProductDetails.as_view(), name='product-details'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add-or-remove-from-cart', views.add_remove_from_cart, name='add-remove-from-cart'),
    path('shipping-address/', views.shipping_address_info, name='shipping-address'),
]