from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Service, Customer, Booking
from .forms import UserRegistrationForm, CustomerProfileForm, BookingForm, BookingStatusForm


def home(request):
    """Home page view"""
    services_count = Service.objects.filter(is_active=True).count()
    bookings_count = Booking.objects.count()
    customers_count = Customer.objects.count()
    
    context = {
        'services_count': services_count,
        'bookings_count': bookings_count,
        'customers_count': customers_count,
    }
    return render(request, 'booking/home.html', context)


def service_list(request):
    """List all available services"""
    services = Service.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    context = {
        'services': services,
        'search_query': search_query,
    }
    return render(request, 'booking/service_list.html', context)


def service_detail(request, pk):
    """Show service details"""
    service = get_object_or_404(Service, pk=pk, is_active=True)
    context = {'service': service}
    return render(request, 'booking/service_detail.html', context)


@login_required
def booking_list(request):
    """List bookings for the logged-in customer"""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        messages.warning(request, 'Please complete your customer profile first.')
        return redirect('booking:profile')
    
    bookings = customer.bookings.all()
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
    }
    return render(request, 'booking/booking_list.html', context)


@login_required
def booking_detail(request, pk):
    """Show booking details"""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        messages.warning(request, 'Please complete your customer profile first.')
        return redirect('booking:profile')
    
    booking = get_object_or_404(Booking, pk=pk, customer=customer)
    context = {'booking': booking}
    return render(request, 'booking/booking_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def create_booking(request):
    """Create a new booking"""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        messages.warning(request, 'Please complete your customer profile first.')
        return redirect('booking:profile')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer
            booking.save()
            booking.calculate_total_price()
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('booking:booking_detail', pk=booking.pk)
    else:
        form = BookingForm()
    
    context = {'form': form}
    return render(request, 'booking/booking_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_booking(request, pk):
    """Edit an existing booking"""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        messages.warning(request, 'Please complete your customer profile first.')
        return redirect('booking:profile')
    
    booking = get_object_or_404(Booking, pk=pk, customer=customer)
    
    # Only allow editing pending bookings
    if booking.status != Booking.PENDING:
        messages.error(request, 'You can only edit pending bookings.')
        return redirect('booking:booking_detail', pk=booking.pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.calculate_total_price()
            booking.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('booking:booking_detail', pk=booking.pk)
    else:
        form = BookingForm(instance=booking)
    
    context = {'form': form, 'booking': booking}
    return render(request, 'booking/booking_form.html', context)


@login_required
@require_http_methods(["POST"])
def delete_booking(request, pk):
    """Delete a booking"""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        messages.warning(request, 'Please complete your customer profile first.')
        return redirect('booking:profile')
    
    booking = get_object_or_404(Booking, pk=pk, customer=customer)
    
    # Only allow deleting pending bookings
    if booking.status != Booking.PENDING:
        messages.error(request, 'You can only delete pending bookings.')
        return redirect('booking:booking_detail', pk=booking.pk)
    
    booking_id = booking.id
    booking.delete()
    messages.success(request, 'Booking deleted successfully!')
    return redirect('booking:booking_list')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('booking:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create customer profile
            Customer.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('booking:login')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'booking/register.html', context)


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('booking:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'booking:home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'booking/login.html')


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('booking:home')


@login_required
def profile(request):
    """User profile view"""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('booking:profile')
    else:
        form = CustomerProfileForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
    }
    return render(request, 'booking/profile.html', context)
