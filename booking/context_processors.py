from .models import Appointment

def latest_booking_context(request):
    """Makes latest booking available to all templates automatically."""
    if request.user.is_authenticated:
        latest_booking = Appointment.objects.filter(user=request.user).order_by('-created_at').first()
    else:
        latest_booking = None
    return {'latest_booking': latest_booking}
