from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

def custom_logout(request):
    print("Logging out user:", request.user)
    return auth_views.LogoutView.as_view()(request)

urlpatterns = [

    path('', views.ticket_list, name='ticket_list'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/create/', views.ticket_create, name='ticket_create'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]