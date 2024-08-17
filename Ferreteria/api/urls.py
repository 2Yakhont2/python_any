from django.urls import path
from . import views

urlpatterns = [
    path("products", views.api_products),
    path("products/<str:pk>", views.api_product)
]
