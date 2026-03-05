from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Service, Customer, Booking
from datetime import datetime, date, time


class ServiceModelTest(TestCase):
    """Test cases for Service model"""
    
    def setUp(self):
        self.service = Service.objects.create(
            name="Haircut",
            description="Professional haircut service",
            price=50.00,
            duration_minutes=30,
            is_active=True
        )
    
    def test_service_creation(self):
        """Test that a service can be created"""
        self.assertEqual(self.service.name, "Haircut")
        self.assertEqual(self.service.price, 50.00)
        self.assertEqual(self.service.duration_minutes, 30)
        self.assertTrue(self.service.is_active)
    
    def test_service_string_representation(self):
        """Test the string representation of a service"""
        self.assertEqual(str(self.service), "Haircut")


class CustomerModelTest(TestCase):
    """Test cases for Customer model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            phone='1234567890',
            city='Test City'
        )
    
    def test_customer_creation(self):
        """Test that a customer can be created"""
        self.assertEqual(self.customer.user.username, 'testuser')
        self.assertEqual(self.customer.phone, '1234567890')
    
    def test_customer_one_to_one_with_user(self):
        """Test the one-to-one relationship with User"""
        self.assertEqual(self.user.customer_profile, self.customer)


class BookingModelTest(TestCase):
    """Test cases for Booking model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer = Customer.objects.create(user=self.user)
        self.service = Service.objects.create(
            name="Haircut",
            description="Haircut service",
            price=50.00,
            duration_minutes=30
        )
        self.booking = Booking.objects.create(
            customer=self.customer,
            booking_date=date.today(),
            booking_time=time(10, 0),
            status=Booking.PENDING
        )
        self.booking.services.add(self.service)
    
    def test_booking_creation(self):
        """Test that a booking can be created"""
        self.assertEqual(self.booking.customer, self.customer)
        self.assertEqual(self.booking.status, Booking.PENDING)
    
    def test_booking_many_to_many_with_service(self):
        """Test the many-to-many relationship with Service"""
        self.assertIn(self.service, self.booking.services.all())
    
    def test_calculate_total_price(self):
        """Test calculating total price"""
        self.booking.calculate_total_price()
        self.assertEqual(self.booking.total_price, 50.00)


class AuthenticationTests(TestCase):
    """Test cases for authentication"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(reverse('booking:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepass123',
            'password2': 'securepass123',
        })
        # Check if user was created (should redirect on success)
        self.assertEqual(response.status_code, 302)
    
    def test_user_login(self):
        """Test user login"""
        response = self.client.post(reverse('booking:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
    
    def test_user_logout(self):
        """Test user logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect


class ViewTests(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer = Customer.objects.create(user=self.user)
        self.service = Service.objects.create(
            name="Test Service",
            description="Test description",
            price=100.00,
            duration_minutes=60
        )
    
    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('booking:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')
    
    def test_service_list_view(self):
        """Test service list view"""
        response = self.client.get(reverse('booking:service_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/service_list.html')
        self.assertIn('services', response.context)
    
    def test_service_detail_view(self):
        """Test service detail view"""
        response = self.client.get(reverse('booking:service_detail', args=[self.service.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/service_detail.html')
    
    def test_booking_list_requires_login(self):
        """Test that booking list requires authentication"""
        response = self.client.get(reverse('booking:booking_list'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
    
    def test_authenticated_booking_list(self):
        """Test booking list for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking:booking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_list.html')
