from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from store.models import Cart, Category, Order, Product


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', context={"products":products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product":product})


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {"category": category, "products": products})


def add_to_cart(request, slug):

    # Recuperamos el usuario
    user = request.user

    # Vamos a abordar dos escenarios
    # 1. El cliente aun no ha agregado ningun producto al carrito pero va a hacerlo.

    # 2. El cliente ya tiene productos en el carrito, pero desea aumentar la cantidad
    # de un producto en especifico.

    # Verificamos si el producto existe o no, si no existe lanzamos un error 404
    product = get_object_or_404(Product, slug=slug)

    # objects.get_or_create >> Este metodo permite crear un elemento (si no existe), 
    # o recuperar un elemento (si existe)

    # Recuperamos el carrito del usuario (si existe) o si no lo creamos
    cart, _ = Cart.objects.get_or_create(user=user)

    # Buscamos en la base de datos si hay un objeto orden que este asociado 
    # al usuario que realiza la solicitud, y a quien corresponde el producto que
    # deseamos agregar
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)

    # Ese metodo devolvera dos cosas: El objeto creado o el objeto recuperado, y
    # la informacion si el objeto fue creado o no.

    # Si el producto se crea = no existia antes, entonces lo agregamos al carrito
    if created:
        cart.orders.add(order)
        cart.save()
    # Si el producto no se crea = existe
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))


def order_checkout(request):
    cart = request.user.cart
    if cart:
        for order in cart.orders.filter(ordered=False):
            order.product.stock -= order.quantity
            order.product.save()
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        cart.orders.clear()
    return redirect('index')


def delete_cart(request):
    cart = request.user.cart
    if cart:
        cart.orders.filter(ordered=False).delete()
    return redirect('index')



def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()
    print(f"Total price calculated: {total_price}")
    return render(request, 'store/cart.html', {'cart': cart, 'orders': cart.orders.all(), 'total_price': total_price})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    total_price = sum(order.get_total_price() for order in orders)
    return render(request, 'store/orders.html', {"orders": orders, "total_price": total_price})
