from django.urls import path, include
from django.contrib import admin
from store.views import cart, category_list, delete_cart, index, order_checkout, order_list, product_detail, add_to_cart

urlpatterns = [
    path('', index, name='index'),
    path('product/<str:slug>/', product_detail, name='product'),
    path('search/<slug:category_slug>/', category_list, name='category'),
    path('product/<str:slug>/add-to-cart', add_to_cart, name='add-to-cart'),
    path('cart/', cart, name="cart"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('cart/checkout/', order_checkout, name="order-checkout"),
    path('orders/', order_list, name='order-list'),
]