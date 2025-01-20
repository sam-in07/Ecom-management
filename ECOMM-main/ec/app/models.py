from django.db import models
from django.contrib.auth.models import User

# Define the choices for the state (regions in Bangladesh)
STATE_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barisal', 'Barisal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
)

# Define the choices for product categories
CATEGORY_CHOICES = (
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('LS', 'Lassi'),
    ('MS', 'Milkshake'),
    ('PN', 'Paneer'),
    ('GH', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice-Creams'),
)

# Define the Product model to store product-related information
class Product(models.Model):
    title = models.CharField(max_length=100)  # Name of the product
    selling_price = models.FloatField()  # Price at which the product is sold
    discounted_price = models.FloatField()  # Discounted price of the product
    description = models.TextField()  # Detailed description of the product
    composition = models.TextField(default='')  # Composition of the product (if applicable)
    prodapp = models.TextField(default='')  # Product application or usage (if applicable)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)  # Category of the product
    product_image = models.ImageField(upload_to='product')  # Image of the product

    def __str__(self):
        return self.title  # Return product title as string representation

# Define the Customer model to store customer-specific information
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (One-to-One)
    name = models.CharField(max_length=200)  # Customer's name
    locality = models.CharField(max_length=200)  # Locality or area where the customer resides
    city = models.CharField(max_length=50)  # City where the customer resides
    mobile = models.IntegerField(default=0)  # Mobile number of the customer
    zipcode = models.IntegerField()  # Postal code for the customer address
    state = models.CharField(choices=STATE_CHOICES, max_length=100)  # State of the customer (from the predefined choices)

    def __str__(self):
        return self.name  # Return customer's name as string representation

# Define the Cart model to store information about items added to the cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (One-to-Many)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product model (One-to-Many)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart

    # Calculate the total cost of the items in the cart (quantity * discounted price)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

# Define the choices for different order statuses
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

# Define the Payment model to store payment details for an order
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    amount = models.FloatField()  # Total payment amount
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay order ID (for payment gateway)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay payment ID (for payment gateway)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)  # Razorpay payment status
    paid = models.BooleanField(default=False)  # Boolean indicating whether the payment has been completed or not

# Define the OrderPlaced model to store the details of a placed order
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (One-to-Many)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to the Customer model (One-to-Many)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product model (One-to-Many)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product ordered
    ordered_date = models.DateTimeField(auto_now_add=True)  # Date and time when the order was placed
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')  # Status of the order
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")  # Link to the Payment model (One-to-Many)

    # Calculate the total cost of the order (quantity * discounted price)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

# Define the Wishlist model to store information about user's wishlisted products
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (One-to-Many)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product model (One-to-Many)
