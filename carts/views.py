from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Helper function to get or create a cart
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def _get_cart_items(request):
    """Helper function to get cart items based on user authentication."""
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        if cart:
            return CartItem.objects.filter(cart=cart, is_active=True)
    return []


def add_cart(request, product_id):
    """Add a product to the cart with optional variations."""
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)  # Get the product

    # Handle product variations
    product_variation = []
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # If the user is authenticated
    if current_user.is_authenticated:
        cart_item_qs = CartItem.objects.filter(product=product, user=current_user)

        # Check if a cart item with the same variations exists
        existing_variations = [list(item.variations.all()) for item in cart_item_qs]
        if product_variation in existing_variations:
            # Increase quantity for the matching cart item
            index = existing_variations.index(product_variation)
            cart_item = cart_item_qs[index]
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Create a new cart item
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if product_variation:
                cart_item.variations.set(product_variation)
                cart_item.save()
    else:
        # Handle anonymous user cart
        cart = Cart.objects.get_or_create(cart_id=_cart_id(request))[0]
        cart_item_qs = CartItem.objects.filter(product=product, cart=cart)

        # Check if a cart item with the same variations exists
        existing_variations = [list(item.variations.all()) for item in cart_item_qs]
        if product_variation in existing_variations:
            # Increase quantity for the matching cart item
            index = existing_variations.index(product_variation)
            cart_item = cart_item_qs[index]
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Create a new cart item
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variation:
                cart_item.variations.set(product_variation)
                cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    """Reduce the quantity of a cart item or remove it if quantity is 1."""
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    """Remove a cart item completely."""
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


def cart(request):
    """Display cart details grouped by vendor."""
    try:
        cart_items = _get_cart_items(request)
        total = 0
        quantity = 0
        vendor_totals = {}

        # Calculate totals and vendor-specific subtotals
        for cart_item in cart_items:
            sub_total = cart_item.product.price * cart_item.quantity
            total += sub_total
            quantity += cart_item.quantity

            vendor = cart_item.product.vendor
            if vendor not in vendor_totals:
                vendor_totals[vendor] = 0
            vendor_totals[vendor] += sub_total

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart_items = []
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0
        vendor_totals = {}

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'vendor_totals': vendor_totals,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    """Display checkout details grouped by vendor."""
    try:
        cart_items = _get_cart_items(request)
        total = 0
        quantity = 0
        vendor_totals = {}

        # Calculate totals and vendor-specific subtotals
        for cart_item in cart_items:
            sub_total = cart_item.product.price * cart_item.quantity
            total += sub_total
            quantity += cart_item.quantity

            vendor = cart_item.product.vendor
            if vendor not in vendor_totals:
                vendor_totals[vendor] = 0
            vendor_totals[vendor] += sub_total

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart_items = []
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0
        vendor_totals = {}

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'vendor_totals': vendor_totals,
    }
    return render(request, 'store/checkout.html', context)
