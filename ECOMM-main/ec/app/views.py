from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Product
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from .models import Cart,Customer,Product
from django.urls import reverse
from django.contrib.auth import logout  # Import the logout method
from django.db.models import Q
from .models import OrderPlaced
from .models import Wishlist




# Create your views here.
def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html", {'totalitem': totalitem})

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/contact.html", {'totalitem': totalitem})



class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/category.html", locals())

class ProductDetail(View):
    def get(self, request, pk):
        # Get the product based on the primary key (pk)
        product = Product.objects.get(pk=pk)
        
        # Initialize the wishlist and cart variables
        wishlist = None
        totalitem = 0

        # If the user is authenticated, get the wishlist and cart
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            totalitem = len(Cart.objects.filter(user=request.user))

        # Render the product detail page with the necessary context
        return render(request, "app/productdetail.html", locals())

def show_wishlist(request):
  user = request.user
  totalitem = 0
  wishitem = 0

  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    wishitem = len(Wishlist.objects.filter(user=request.user))

  product = Wishlist.objects.filter(user=user)
  return render(request, "app/wishlist.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):

        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
        else:
            messages.warning(request, "Invalid input data. Please correct the errors.")
        return render(request, 'app/customerregistration.html', {'form': form})


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcode=zipcode
            )
            reg.save()
            messages.success(request, "Congratulations! Profile saved successfully.")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')

# Add logout functionality
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to home or login page


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))  # Redirect to the home page (or any other page)

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))  # Redirect to the home page (or any other page)
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0

    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value

    totalamount = amount + 60
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/addtocart.html', locals())

def calculate_cart_total(user):
    """
    Helper function to calculate the total amount and total quantity in the cart.
    """
    cart = Cart.objects.filter(user=user)
    amount = 0
    for item in cart:
        amount += item.quantity * item.product.discounted_price
    totalamount = amount + 60  # Add shipping cost
    return amount, totalamount

class checkout(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 60
        return render(request, 'app/checkout.html', locals())

def plus_cart(request):
    if request.method == 'GET':

        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.quantity += 1  # Increment quantity
        c.save()

        # Calculate updated totals
        amount, totalamount = calculate_cart_total(request.user)

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        if c.quantity > 1:  # Ensure quantity doesn't go below 1
            c.quantity -= 1
            c.save()
        else:
            c.delete()  # Remove the item if quantity is 0

        # Calculate updated totals
        amount, totalamount = calculate_cart_total(request.user)

        data = {
            'quantity': c.quantity if c.pk else 0,  # Return 0 if the item was deleted
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()  # Remove the item from the cart

        # Calculate updated totals
        amount, totalamount = calculate_cart_total(request.user)

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()

        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()

        data = {
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
    








