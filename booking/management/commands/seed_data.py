from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import Service, Customer, Booking
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Seed the database with initial sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Created superuser (admin)'))
        
        # Create sample users
        if not User.objects.filter(username='john_doe').exists():
            user1 = User.objects.create_user(
                username='john_doe',
                email='john@example.com',
                password='testpass123',
                first_name='John',
                last_name='Doe'
            )
            Customer.objects.create(
                user=user1,
                phone='5551234567',
                address='123 Main St',
                city='New York',
                postal_code='10001'
            )
            self.stdout.write(self.style.SUCCESS('✓ Created user: john_doe'))
        
        if not User.objects.filter(username='jane_smith').exists():
            user2 = User.objects.create_user(
                username='jane_smith',
                email='jane@example.com',
                password='testpass123',
                first_name='Jane',
                last_name='Smith'
            )
            Customer.objects.create(
                user=user2,
                phone='5559876543',
                address='456 Oak Ave',
                city='Los Angeles',
                postal_code='90001'
            )
            self.stdout.write(self.style.SUCCESS('✓ Created user: jane_smith'))
        
        # Create sample services
        services_data = [
            {
                'name': 'Haircut',
                'description': 'Professional haircut service for men and women',
                'price': 45.00,
                'duration_minutes': 30
            },
            {
                'name': 'Hair Color',
                'description': 'Professional hair coloring and dyeing service',
                'price': 75.00,
                'duration_minutes': 60
            },
            {
                'name': 'Facial',
                'description': 'Relaxing facial treatment with premium products',
                'price': 60.00,
                'duration_minutes': 45
            },
            {
                'name': 'Massage',
                'description': 'Full body massage therapy service',
                'price': 80.00,
                'duration_minutes': 60
            },
            {
                'name': 'Manicure',
                'description': 'Professional nail care and manicure service',
                'price': 30.00,
                'duration_minutes': 30
            },
            {
                'name': 'Pedicure',
                'description': 'Professional nail care for feet',
                'price': 40.00,
                'duration_minutes': 40
            },
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'description': service_data['description'],
                    'price': service_data['price'],
                    'duration_minutes': service_data['duration_minutes'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service.name}'))
        
        # Create sample bookings
        user1 = User.objects.get(username='john_doe')
        customer1 = user1.customer_profile
        service1 = Service.objects.get(name='Haircut')
        service2 = Service.objects.get(name='Hair Color')
        
        if not Booking.objects.filter(customer=customer1).exists():
            booking1 = Booking.objects.create(
                customer=customer1,
                booking_date=date.today() + timedelta(days=3),
                booking_time=time(10, 0),
                status=Booking.CONFIRMED,
                notes='Please cut short on sides'
            )
            booking1.services.add(service1)
            booking1.calculate_total_price()
            booking1.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created booking for john_doe'))
            
            booking2 = Booking.objects.create(
                customer=customer1,
                booking_date=date.today() + timedelta(days=5),
                booking_time=time(14, 30),
                status=Booking.PENDING,
                notes='Want to try dark brown color'
            )
            booking2.services.add(service2)
            booking2.calculate_total_price()
            booking2.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created second booking for john_doe'))
        
        self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
        self.stdout.write(self.style.WARNING('\nTest Credentials:'))
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('User: john_doe / testpass123')
        self.stdout.write('User: jane_smith / testpass123')
