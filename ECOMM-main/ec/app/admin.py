from django.contrib import admin
from .models import Payment
from .models import OrderPlaced

from .models import Cart, Customer, Product, Wishlist  # Ensure both models are imported

# Register your models here.

# Registering the Product model to be manageable via the Django admin interface
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    # Specifies which fields will be displayed in the list view of the Product model
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

# Registering the Customer model to be manageable via the Django admin interface
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    # Specifies which fields will be displayed in the list view of the Customer model
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

# Registering the Cart model to be manageable via the Django admin interface
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    # Specifies which fields will be displayed in the list view of the Cart model
    list_display = ['id', 'user', 'product', 'quantity']

# Registering the Payment model to be manageable via the Django admin interface
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    # Specifies which fields will be displayed in the list view of the Payment model
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

# Registering the OrderPlaced model to be manageable via the Django admin interface
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    # Specifies which fields will be displayed in the list view of the OrderPlaced model
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']

# Registering the Wishlist model to be manageable via the Django admin interface
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    # Specifies which fields will be displayed in the list view of the Wishlist model
    list_display = ['id', 'user', 'product']
