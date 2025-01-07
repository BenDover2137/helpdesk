from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/delete/<int:pk>/', views.delete_ticket, name='delete_ticket'),
    path('', views.profile, name='ticket_list'),
    path('ticket/create/', views.ticket_create, name='ticket_create'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', views.custom_login, name='login'),  # Ensure this matches LOGIN_URL
    path('register/', views.register, name='register'),

]