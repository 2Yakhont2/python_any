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


    # Verificar si el producto está activo y tiene stock disponible
    if not product.is_active or product.stock <= 0:
        return redirect('product', slug=slug)
    
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    # Si el producto no se crea = existe
    else:
        if order.quantity + 1 <= product.stock:
            order.quantity += 1
            order.save()
        else:
            # Mostrar un mensaje de que no hay stock suficiente
            return redirect('product', slug=slug)

    return redirect(reverse("product", kwargs={"slug": slug}))


def order_checkout(request):
    cart = request.user.cart
    if cart:
        for order in cart.orders.filter(ordered=False):
            if order.quantity > order.product.stock:
                # No procesar el checkout si no hay stock suficiente
                return redirect('cart')
            
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

    if not cart.orders.exists():
        return redirect('index')

    total_price = cart.get_total_price()
    print(f"Total price calculated: {total_price}")
    return render(request, 'store/cart.html', {'cart': cart, 'orders': cart.orders.all(), 'total_price': total_price})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    total_price = sum(order.get_total_price() for order in orders)
    return render(request, 'store/orders.html', {"orders": orders, "total_price": total_price})
