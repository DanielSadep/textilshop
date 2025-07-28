from apps.cart.models import CartItem

def cart_summary(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    items = CartItem.objects.filter(session_key=session_key)
    total_items = sum(item.quantity for item in items)

    return {
        'cart_total_items': total_items
    }

