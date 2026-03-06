def calculate_booking_duration(services):
    """Calculate total duration for multiple services."""
    return sum(service.duration_minutes for service in services)

def format_price(price):
    """Format price with currency symbol."""
    return f"${price:,.2f}"