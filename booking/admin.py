from django.contrib import admin
from .models import Service, Customer, Booking


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_minutes', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'created_at']
    ordering = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'phone', 'city', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone']
    list_filter = ['city', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'booking_date', 'booking_time', 'status', 'total_price']
    search_fields = ['customer__user__first_name', 'customer__user__last_name', 'customer__user__email']
    list_filter = ['status', 'booking_date', 'created_at']
    filter_horizontal = ['services']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    fieldsets = (
        ('Booking Info', {
            'fields': ('customer', 'booking_date', 'booking_time', 'status')
        }),
        ('Services', {
            'fields': ('services', 'total_price')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
