from django.db import models
from django.conf import settings  # To reference the Account model for vendors
from decimal import Decimal
from category.models import Category

# Shipping choices for products
FULFILLMENT_CHOICES = [
    ('seller', 'Fulfilled by Seller'),
    ('company', 'Fulfilled by Company'),
]

# Delivery choices for products
DELIVERY_CHOICES = [
    ('selected_countries', 'Selected Countries'),
    ('worldwide', 'Worldwide Delivery'),
    ('local', 'Local Delivery'),
]

# Define the Product model
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    # Associate each product with a vendor (Account model)
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'vendor'}
    )

    product_description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for currency values
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    # Category association
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Time-related fields
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Shipping-related fields
    fulfillment_by = models.CharField(
        max_length=10, 
        choices=FULFILLMENT_CHOICES, 
        default='seller'
    )
    delivery_option = models.CharField(
        max_length=20, 
        choices=DELIVERY_CHOICES, 
        default='worldwide'
    )

    # Product variants (we'll use JSONField for flexibility)
    variants = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Store variants like color, size, etc. as a JSON object"
    )

    def __str__(self):
        return self.product_name

    # Optional: Method to calculate discounted prices, etc.
    def get_price(self):
        return self.price

    # Optional: Method to get the vendor's store name
    @property
    def vendor_store_name(self):
        return self.vendor.store_name if self.vendor and hasattr(self.vendor, 'store_name') else "Unknown Vendor"


# Define the Service model
class Service(models.Model):
    service_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    # Associate each service with a vendor (Account model)
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'vendor'}
    )

    service_description = models.TextField(max_length=500, blank=True)

    # Pricing for services (could be hourly, per session, etc.)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for currency values
    is_available = models.BooleanField(default=True)

    # Category association (can be a service-specific category)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Time-related fields
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

    # Optional: Method to get the vendor's store name
    @property
    def vendor_store_name(self):
        return self.vendor.store_name if self.vendor and hasattr(self.vendor, 'store_name') else "Unknown Vendor"

    # Optional: Method to calculate service pricing logic, like discounts or custom rates
    def get_price(self):
        return self.price