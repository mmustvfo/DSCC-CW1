# Project File Structure

DSCC-CW1/
├── booking/                              # Django booking app
│   ├── __init__.py
│   ├── admin.py                         # Admin configuration (Service, Customer, Booking)
│   ├── apps.py                          # App configuration
│   ├── forms.py                         # Forms (Registration, Profile, Booking)
│   ├── models.py                        # Models (Service, Customer, Booking)
│   ├── tests.py                         # Test cases
│   ├── urls.py                          # URL routing
│   ├── views.py                         # Views (11 views total)
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py             # Initial migration
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── seed_data.py             # Management command for sample data
│
├── booking_project/                     # Django project settings
│   ├── __init__.py
│   ├── settings.py                      # Django settings (database, apps, middleware)
│   ├── urls.py                          # Project URL configuration
│   └── wsgi.py                          # WSGI application
│
├── templates/                           # HTML templates
│   ├── base.html                        # Base template with navigation
│   └── booking/
│       ├── home.html                    # Home page
│       ├── register.html                # User registration
│       ├── login.html                   # User login
│       ├── profile.html                 # User profile
│       ├── service_list.html            # Service listings
│       ├── service_detail.html          # Service details
│       ├── booking_list.html            # Booking list
│       ├── booking_detail.html          # Booking details
│       └── booking_form.html            # Booking form (create/edit)
│
├── static/                              # Static files
│   └── css/
│       └── style.css                    # Custom CSS styling
│
├── nginx/                               # Nginx configuration
│   └── nginx.conf                       # Nginx server configuration
│
├── manage.py                            # Django management script
├── requirements.txt                     # Python dependencies
├── .env                                 # Environment variables
├── .gitignore                           # Git ignore file
├── Dockerfile                           # Docker image definition
├── docker-compose.yml                   # Docker Compose configuration
├── initialize.sh                        # Initialization shell script
├── COMMITS.md                           # Commit history documentation
└── README.md                            # Project documentation

## File Statistics

- **Total Files**: 40+
- **Total Lines of Code**: 2500+
- **Python Files**: 20+
- **HTML Templates**: 10
- **Configuration Files**: 6

## Key Files and Their Purpose

### Models (booking/models.py)
- Service: Represents available services
- Customer: Customer information linked to User
- Booking: Booking records with relationships

### Views (booking/views.py)
- home: Home page with statistics
- service_list: List all services with search
- service_detail: Show service details
- booking_list: List user's bookings with filters
- booking_detail: Show booking details
- create_booking: Create new booking
- edit_booking: Edit existing booking
- delete_booking: Delete booking
- register: User registration
- user_login: User authentication
- user_logout: Session termination
- profile: User profile management

### Forms (booking/forms.py)
- UserRegistrationForm: Registration form
- CustomerProfileForm: Profile update form
- BookingForm: Booking creation/edit form
- BookingStatusForm: Status update form

### Templates
- base.html: Navigation and layout
- home.html: Dashboard
- register.html: Registration form
- login.html: Login form
- profile.html: User profile
- service_list.html: Service list with search
- service_detail.html: Service information
- booking_list.html: User bookings
- booking_detail.html: Booking details
- booking_form.html: Booking form

### Configuration
- settings.py: Django configuration
- urls.py (Project): Route to booking app
- urls.py (Booking): Booking app routes
- docker-compose.yml: Multi-container setup
- nginx.conf: Web server configuration
- Dockerfile: Container image

## Database Models Relationships

```
User (Django)
    └─ OneToOne ─→ Customer
         └─ OneToMany ─→ Booking
              └─ ManyToMany ─→ Service
```

## Features Implemented

✓ User Authentication (Register, Login, Logout)
✓ Service Management (Create, List, Detail)
✓ Booking System (CRUD operations)
✓ Admin Panel (Full management)
✓ Search Functionality (Services)
✓ Filtering (Bookings by status)
✓ Responsive Design (Bootstrap 5)
✓ Form Validation
✓ Error Handling
✓ Environment Configuration
✓ Docker Containerization
✓ Static Files Management
✓ Database Migrations

## Development Workflow

1. **Local Development**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. **Database Seeding**
   ```bash
   python manage.py seed_data
   ```

3. **Docker Deployment**
   ```bash
   docker-compose up --build
   ```

## Testing

Run tests with:
```bash
python manage.py test
```

Test coverage includes:
- Model creation and relationships
- User authentication
- View access and permissions
- Form validation
- Database operations

## Security Features

- CSRF protection on all forms
- Password hashing
- User authentication required for bookings
- Admin panel protection
- SQL injection prevention (Django ORM)
- XSS protection (template escaping)

## Performance Optimizations

- Static file optimization with Nginx
- Database indexing through models
- Query optimization with select_related/prefetch_related
- Caching headers for static files
- Responsive image loading

## Deployment Scenarios

1. **Development**: SQLite3, local server
2. **Testing**: SQLite3, Gunicorn
3. **Production**: PostgreSQL, Docker, Nginx
