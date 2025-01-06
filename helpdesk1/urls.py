from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tickets import views as ticket_views  # Import the register view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls')),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', ticket_views.custom_logout, name='logout'),
    path('register/', ticket_views.register, name='register'),  # Registration URL
    path('accounts/profile/', ticket_views.profile, name='profile'),
]