from django.urls import path
from . import views
from .views import user_logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

# URL patterns for the application
urlpatterns = [
    # Home page route
    path("", views.home),  # Directs to the home page view

    # Static pages routes (about and contact)
    path("about/", views.about, name="about"),  # About page route
    path("contact/", views.contact, name="contact"),  # Contact page route

    # Category-based views
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),  # Category based on slug
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),  # Category by title

    # Product details page
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),  # Product detail page based on primary key (pk)

    # Profile-related views
    path('profile/', views.ProfileView.as_view(), name='profile'),  # User profile page
    path('address/', views.address, name='address'),  # User address page
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),  # Update address page

    # Cart management views
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),  # Add product to the cart
    path('cart/', views.show_cart, name='showcart'),  # Show cart page
    path('checkout/', views.checkout.as_view(), name='checkout'),  # Checkout page

    # Cart operations like increasing/decreasing quantity and removal
    path('pluscart/', views.plus_cart),  # Increase product quantity in the cart
    path('minuscart/', views.minus_cart),  # Decrease product quantity in the cart
    path('removecart/', views.remove_cart),  # Remove product from the cart
    path('orders/', views.orders, name='orders'),  # View past orders

    # Wishlist management views
    path('pluswishlist/', views.plus_wishlist),  # Add product to wishlist
    path('minuswishlist/', views.minus_wishlist),  # Remove product from wishlist

    # Wishlist display page
    path('wishlist/', views.show_wishlist, name='showwishlist'),  # View the wishlist

    # Customer registration route
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),  # Customer registration page

    # Authentication views
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),  # Login page with custom login form

    # Password change functionality
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),  # Change password view
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),  # Success page after password change

    # Logout view
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),  # Logout and redirect to login page

    # Password reset functionality
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),  # Password reset request page
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),  # Password reset done page
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),  # Password reset confirmation page
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),  # Completion page for password reset

    # Custom logout route (duplicate of Django's built-in logout)
    path('logout/', user_logout, name='logout'),  # Custom logout functionality
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files during development
