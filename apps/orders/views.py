from django.shortcuts import redirect, render
from apps.cart.models import CartItem
from .models import Order, OrderItem
from django.shortcuts import get_object_or_404, render
from .models import Order

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

def create_order(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        return render(request, 'orders/order_error.html', {'message': 'Tu carrito está vacío.'})

    # Calcular total del pedido
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Crear la orden con total
    order = Order.objects.create(
        customer_name="Cliente Genérico",
        customer_email="cliente@example.com",
        total=total
    )

    # Crear los ítems de la orden
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Limpiar el carrito
    cart_items.delete()

    return render(request, 'orders/order_success.html', {'order': order})
