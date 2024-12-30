from django.db import models
from store.models import Product, Variation
from accounts.models import Account


class Cart(models.Model):
    """Represents a shopping cart that can be associated with a user or anonymous session."""
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, blank=True)  # For anonymous carts
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user})" if self.user else f"Cart (ID: {self.cart_id})"

    def total_items(self):
        """Calculate the total number of items in the cart."""
        return sum(item.quantity for item in self.cartitem_set.all())

    def total_price(self):
        """Calculate the total price of all items in the cart."""
        return sum(item.sub_total() for item in self.cartitem_set.all())

    def vendor_totals(self):
        """Calculate subtotals grouped by vendor."""
        vendor_totals = {}
        for item in self.cartitem_set.all():
            vendor = item.product.vendor  # Assuming Product has a `vendor` field
            vendor_totals[vendor] = vendor_totals.get(vendor, 0) + item.sub_total()
        return vendor_totals


class CartItem(models.Model):
    """Represents a single item in the cart."""
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)  # Optional for anonymous users
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        """Calculate the subtotal for this cart item."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"
