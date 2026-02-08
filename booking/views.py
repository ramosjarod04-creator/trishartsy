from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment, CustomUser
from django.db import IntegrityError
from .models import UploadedArt
from django.contrib import admin


# ===============================
# CUSTOMER BOOKING
# ===============================
def book_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Please log in before booking.")
            return redirect('login')

        # Use the form with POST and FILES data
        form = AppointmentForm(request.POST, request.FILES)
        
        # Debug: Print what we received
        print(f"DEBUG - Files in request.FILES:")
        print(f"  art_image: {request.FILES.get('art_image')}")
        print(f"  payment_reference: {request.FILES.get('payment_reference')}")
        print(f"DEBUG - Form is valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"DEBUG - Form errors: {form.errors}")
        
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.status = 'Pending'
            appointment.save()
            
            print(f"DEBUG - Appointment saved:")
            print(f"  ID: {appointment.id}")
            print(f"  art_image: {appointment.art_image}")
            print(f"  payment_reference: {appointment.payment_reference}")

            messages.success(request, "Booking submitted! Wait for admin approval.")
            return redirect('gallery')
        else:
            messages.error(request, "Error submitting booking. Please check your inputs.")
            print(f"Form errors: {form.errors}")
    else:
        form = AppointmentForm()

    return render(request, 'booking/book.html', {'form': form})


# ===============================
# ADMIN DASHBOARD
# ===============================
@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or getattr(request.user, "role", None) == "admin"):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('gallery')

    appointments = Appointment.objects.all().order_by('-created_at')
    return render(request, 'booking/admin_dashboard.html', {'appointments': appointments})


@login_required
def accept_booking(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check if already exists to avoid duplicates
    existing = UploadedArt.objects.filter(
        client_name=appointment.fullname,
        contact=appointment.contact
    ).first()
    
    if not existing and (appointment.art_image or appointment.payment_reference):
        # Create the UploadedArt entry with the image files
        UploadedArt.objects.create(
            client_name=appointment.fullname,
            contact=appointment.contact,
            art=appointment.art_image,  # This will copy the file
            reference=appointment.payment_reference  # This will copy the file
        )
        print(f"DEBUG - Created UploadedArt for {appointment.fullname}")
    
    # Update status after creating UploadedArt
    appointment.status = 'Accepted'
    appointment.save()

    messages.success(request, f"{appointment.fullname}'s booking has been accepted and added to the gallery.")
    return redirect('admin_dashboard')

@login_required
def deny_booking(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'Denied'
    appointment.save()
    return redirect('admin_dashboard')


# ===============================
# AUTHENTICATION VIEWS
# ===============================
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('gallery')

    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not fullname or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'booking/signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'booking/signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'booking/signup.html')

        try:
            names = fullname.split(" ", 1)
            first_name = names[0]
            last_name = names[1] if len(names) > 1 else ""

            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='customer'
            )
            user.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "There was an error creating your account. Try again.")
            return render(request, 'booking/signup.html')

    return render(request, 'booking/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or getattr(request.user, "role", None) == "admin":
            return redirect('admin_dashboard')
        else:
            return redirect('gallery')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                user_obj = CustomUser.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")

            if user.is_superuser or getattr(user, "role", None) == "admin":
                return redirect('admin_dashboard')
            else:
                return redirect('gallery')
        else:
            messages.error(request, "Invalid username/email or password.")

    return render(request, 'booking/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# ===============================
# MAIN SITE PAGES
# ===============================
@login_required(login_url='login')
def gallery_view(request):
    """Home page (Customer Gallery)"""
    latest_booking = Appointment.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, 'booking/gallery.html', {'latest_booking': latest_booking})


def about_view(request):
    """About page"""
    return render(request, 'booking/about.html')


# ===============================
# ROOT REDIRECT (on server start)
# ===============================
def home_redirect(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@login_required
def admin_gallery(request):
    """Admin Gallery View – show all uploads and pending bookings"""
    if not (request.user.is_superuser or getattr(request.user, "role", None) == "admin"):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('gallery')
    
    uploads = UploadedArt.objects.all().order_by('-date_uploaded')
    appointments = Appointment.objects.exclude(status='Accepted').order_by('-created_at')

    return render(request, 'booking/admin_gallery.html', {
        'uploads': uploads,
        'appointments': appointments,
    })


@admin.register(UploadedArt)
class UploadedArtAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'date_uploaded')