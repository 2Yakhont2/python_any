from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from store.models import Product
from rest_framework.response import Response

# Create your views here.

@api_view()
def api_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view()
def api_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
