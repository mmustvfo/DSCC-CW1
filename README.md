# Django Booking System - DSCC Coursework 1

A comprehensive Django web application demonstrating professional full-stack development practices including containerization, CI/CD pipelines, and cloud deployment.

**Coursework Deadline:** March 5, 2026, 23:59
**Student ID:** [Your Student ID]

---

## 📋 Project Overview

**Django Booking System** is a professional web application built with Django 6.0 that allows users to browse services, create bookings, and manage their reservations. The application demonstrates modern DevOps practices including Docker containerization, automated testing, and GitHub Actions CI/CD pipeline.

### Key Features

- **User Authentication**: Registration, login, logout, profile management
- **Service Management**: Browse and search available services with detailed information
- **Booking System**: Create, view, edit, and cancel bookings with real-time pricing
- **Admin Panel**: Comprehensive Django admin interface for managing services, customers, and bookings
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Database Relationships**: OneToOne (User↔Customer), ForeignKey (Booking→Customer), ManyToMany (Booking↔Service)
- **Production Ready**: Containerized with Docker, deployed with Nginx & Gunicorn

---

## 🛠️ Technologies & Stack

### Backend
- **Framework**: Django 6.0.3
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: Django ORM
- **Forms**: django-crispy-forms with Bootstrap 5
- **Authentication**: Django built-in auth system

### Frontend
- **Template Engine**: Django Templates
- **Styling**: Bootstrap 5
- **CSS**: Custom styling with responsive design
- **JavaScript**: jQuery (admin dashboard)

### DevOps & Deployment
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (reverse proxy)
- **App Server**: Gunicorn (WSGI application server)
- **CI/CD**: GitHub Actions
- **Testing**: pytest-django
- **Code Quality**: flake8, black

### Version Control & Infrastructure
- **Repository**: GitHub (public)
- **Deployment**: Eskiz Cloud Server
- **SSL/HTTPS**: Let's Encrypt

---

## 📊 Database Schema

### Models & Relationships

**Service Model**
```
- id (BigAutoField, Primary Key)
- name (CharField, max_length=100)
- description (TextField)
- price (DecimalField, max_digits=8, decimal_places=2)
- duration_minutes (IntegerField)
- is_active (BooleanField)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```

**Customer Model**
```
- id (BigAutoField, Primary Key)
- user (OneToOneField → User)
- phone (CharField)
- address (TextField)
- city (CharField)
- postal_code (CharField)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```

**Booking Model**
```
- id (BigAutoField, Primary Key)
- customer (ForeignKey → Customer)
- services (ManyToManyField → Service)
- booking_date (DateField)
- booking_time (TimeField)
- status (CharField: pending/confirmed/completed/cancelled)
- notes (TextField, optional)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```

### Relationships
- **OneToOne**: User ↔ Customer (profile extension pattern)
- **ForeignKey**: Booking → Customer (cardinality 1:N)
- **ManyToMany**: Booking ↔ Service (multiple services per booking)

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.12+
- pip and virtual environment
- Git

### Step-by-Step Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/DSCC-CW1.git
cd DSCC-CW1
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Apply database migrations**
```bash
python manage.py migrate
```

6. **Create superuser (admin account)**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python manage.py seed_data
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit: http://localhost:8000

### Test Credentials (After seed_data)
- **Admin**: admin / admin123
- **User 1**: john_doe / testpass123
- **User 2**: jane_smith / testpass123

---

## 🐳 Docker Setup & Local Containerization

### Build and Run with Docker

1. **Build Docker image**
```bash
docker build -t dscc-booking:latest .
```

2. **Run with Docker Compose**
```bash
docker-compose up -d
```

3. **Access the application**
```
Web App: http://localhost:8000
Admin Panel: http://localhost:8000/admin
Nginx: http://localhost:80
```

### Docker Compose Services

**Services Configuration:**
- **Django App** (web): Port 8000, Gunicorn server
- **PostgreSQL** (db): Port 5432, database persistence
- **Nginx** (nginx): Port 80, static file serving & reverse proxy

### Environment Variables for Docker

Create `.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DB_ENGINE=django.db.backends.postgresql
DB_NAME=booking_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Docker Image Specifications
- **Base Image**: python:3.12-alpine
- **Multi-stage Build**: Optimized for production
- **Non-root User**: Security best practice (appuser)
- **Image Size**: 167MB (well under 200MB requirement)
- **Layer Caching**: Optimized for faster rebuilds

---

## 📈 Deployment to Production (Eskiz Server)

### Prerequisites
- Registered domain name
- Eskiz cloud server access
- SSH credentials

### Deployment Steps

1. **Configure server firewall (UFW)**
```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

2. **Install Docker and Docker Compose**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone repository on server**
```bash
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/DSCC-CW1.git
cd DSCC-CW1
```

4. **Configure production environment**
```bash
cp .env.production .env
# Edit with production values
```

5. **Set up SSL certificate (Let's Encrypt)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --standalone -d yourdomain.com
# Copy certificates to project: nginx/certs/
```

6. **Start services**
```bash
docker-compose -f docker-compose.yml up -d
```

7. **Run migrations in production**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

### Pipeline Overview

The automated workflow (`.github/workflows/ci-cd.yml`) includes:

1. **Code Quality Checks**
   - flake8 linting
   - black code formatting
   
2. **Automated Testing**
   - pytest-django with minimum 5 tests
   - Coverage reporting

3. **Docker Image Build & Push**
   - Build optimized image
   - Tag with commit SHA and "latest"
   - Push to Docker Hub registry

4. **Automated Deployment**
   - SSH to production server
   - Pull latest images
   - Run database migrations
   - Restart containers with zero downtime

### GitHub Secrets Configuration

Required secrets in repository settings:
- `DOCKERHUB_USERNAME`: Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token
- `SSH_PRIVATE_KEY`: SSH private key for server access
- `SSH_HOST`: Production server IP/hostname
- `SSH_USERNAME`: SSH username for production server

### Workflow Trigger
- Automatically runs on `git push` to `main` branch
- Manual trigger available via Actions tab

---

## ✅ Testing

### Running Tests Locally

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=booking --cov-report=html

# Run specific test file
pytest booking/tests/test_models.py -v
pytest booking/tests/test_views.py -v
```

### Test Requirements
- **Minimum 5 tests** covering critical functionality
- Model tests (Service, Customer, Booking creation)
- View tests (authentication, CRUD operations)
- Form validation tests
- All tests integrated into CI/CD pipeline

### Test Coverage Areas
1. User registration and authentication
2. Service listing and filtering
3. Booking creation with validation
4. Booking editing and deletion
5. Profile management

---

## 📁 Project Structure

```
DSCC-CW1/
├── booking/                      # Main Django app
│   ├── migrations/              # Database migrations
│   ├── admin.py                 # Admin panel configuration
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── forms.py                 # Django forms
│   ├── urls.py                  # URL routing
│   ├── tests/                   # Pytest test suite
│   │   ├── test_models.py      # Model tests
│   │   ├── test_views.py       # View tests
│   │   └── test_hello.py       # Basic test
│   └── management/              # Custom commands
│
├── booking_project/             # Project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Project URL config
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
│
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   └── booking/                # App templates
│
├── static/                      # Static files
│   ├── css/                    # Custom stylesheets
│   └── img/                    # Images
│
├── nginx/                       # Nginx configuration
│   └── nginx.conf              # Reverse proxy config
│
├── Dockerfile                   # Multi-stage build
├── docker-compose.yml          # Service orchestration
├── requirements.txt            # Python dependencies
├── manage.py                   # Django CLI
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── COMMITS.md                  # Commit documentation
└── TECHNICAL_REPORT.md         # Technical report (submitted separately)
```

---

## 📋 Environment Variables Documentation

### Development Environment (.env)
```
# Django Settings
SECRET_KEY=django-insecure-dev-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email (optional for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production Environment
```
# Django Settings
SECRET_KEY=<strong-random-key-here>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=booking_db
DB_USER=postgres
DB_PASSWORD=<strong-db-password>
DB_HOST=db
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<app-password>
```

### Generating SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 📞 Features Demonstration

### Authentication Flow
1. User navigates to registration page
2. Enters email, username, password (validated)
3. Account created with Customer profile
4. Can now login and access booking features

### Booking Workflow
1. Browse services on homepage (search & filter available)
2. View service details with pricing and duration
3. Click "Book Now" → Create booking
4. Select date, time, and services
5. Booking created with total price calculated
6. View in "My Bookings" dashboard
7. Edit or cancel pending bookings

### Admin Panel
- Dashboard with statistics
- Manage Services (create, update, deactivate)
- Manage Customers (view profiles)
- Manage Bookings (track status, update)
- Bulk actions and filtering

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate booking zero

# Recreate migrations
python manage.py makemigrations booking
python manage.py migrate
```

### Docker Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

---

## 📚 Technologies Reference

| Component | Version | Purpose |
|-----------|---------|---------|
| Django | 6.0.3 | Web framework |
| Python | 3.12+ | Runtime |
| PostgreSQL | 15-alpine | Production database |
| Docker | Latest | Containerization |
| Nginx | alpine | Reverse proxy |
| Gunicorn | 22.0.0 | WSGI server |
| Bootstrap | 5 | Frontend framework |
| pytest | 7.4.3 | Testing framework |
| pytest-django | 4.7.0 | Django test integration |

---

## 📄 Licensing & Attribution

This project is submitted as coursework for DSCC Module (University of [Institution]).

### Dependencies
- Django: BSD License
- Bootstrap: MIT License
- All other packages: See requirements.txt for details

---

## 👤 Student Information

- **Name**: [Your Full Name]
- **Student ID**: [Your Student ID]
- **Course**: [Course Code: DSCC]
- **Submission Date**: March 5, 2026
- **GitHub Repository**: https://github.com/YOUR_USERNAME/DSCC-CW1

---

## 📞 Support & Questions

For issues or questions about this project:
1. Check existing GitHub Issues
2. Review COMMITS.md for development history
3. Consult TECHNICAL_REPORT.md for architecture details
4. Contact: [your-email@institution.edu]

---

**Last Updated**: March 5, 2026
**Status**: Production Ready ✅
