from django.shortcuts import get_object_or_404, redirect, render
from apps.products.models import Product
from .models import CartItem

def add_to_cart(request, product_id):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:view_cart')  # ✅ nombre correcto

def cart_detail(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })
