from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

def custom_logout(request):
    print("Logging out user:", request.user)  # Debug statement
    return auth_views.LogoutView.as_view()(request)

urlpatterns = [
    # Ticket-related URLs
    path('', views.ticket_list, name='ticket_list'),  # List all tickets
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),  # View a single ticket
    path('ticket/create/', views.ticket_create, name='ticket_create'),  # Create a new ticket
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # Authentication URLs (optional, if you want to keep them in the tickets app)
    # Note: These are already included in the main `helpdesk/urls.py`, so you don't need to repeat them here.
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('register/', views.register, name='register'),
]