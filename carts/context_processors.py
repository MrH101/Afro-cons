from collections import defaultdict
from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    """Context processor to calculate cart item count and vendor-specific totals."""
    cart_count = 0
    vendor_totals = defaultdict(float)  # Dictionary to store vendor subtotals

    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            # Get all cart items for the authenticated user
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Get the cart for the session ID
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            else:
                cart_items = []

        # Calculate total quantity and vendor-specific totals
        for cart_item in cart_items:
            cart_count += cart_item.quantity
            vendor = cart_item.product.vendor  # Assuming `vendor` is a field on the `Product` model
            vendor_totals[vendor] += cart_item.sub_total()

    except Exception as e:
        cart_count = 0

    return {
        'cart_count': cart_count,
        'vendor_totals': dict(vendor_totals),  # Convert defaultdict to a regular dict
    }
