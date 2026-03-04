from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Services
    path('services/', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    
    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/<int:pk>/edit/', views.edit_booking, name='edit_booking'),
    path('bookings/<int:pk>/delete/', views.delete_booking, name='delete_booking'),
]
